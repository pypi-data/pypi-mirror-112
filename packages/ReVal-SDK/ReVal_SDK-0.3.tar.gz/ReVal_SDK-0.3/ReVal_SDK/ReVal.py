import torch
import torch.nn.functional as F
import numpy as np
import re
import json
import os
from progress.bar import Bar
import decimal

import matplotlib.pyplot as pyplot
import matplotlib.transforms as transforms

class ReVal():
    def __init__(self, model, model_name, model_file_name, model_version, backend_type):
        """ Reval Init
        Args:
            model (model): Model object
            model_file_name (str): Filename of model
            model_version (str): Version of model
            backend_type (str): Backend type required to see if using test, triton, or tensorFlow
        """
        self.model = model.eval()
        self.model_name = model_name
        self.model_version = model_version

        if '.' in model_file_name:
            self.model_file_name = model_file_name
            self.model_file_extension = model_file_name.split('.')[1]
        else:
            raise Exception("Please enter a valid model_file_name (ex. \"saved_model.pb\"")

        if backend_type == "triton" or backend_type == "tensorFlow" or backend_type == "test":        
            self.backend_type = backend_type
        else:
            raise Exception("backend_type not supported. Available Options = [\"triton\", \"tensorFlow\", or \"test\"]")

    def validate(self, retina, validation_set, difference_threshold=1e-3, batching_maxSize=8):
        """ Export model, start inference server, validate inference, stop inference server, compare results
        Args:
            retina (retina): Instance of the retina class
            validation_set (dataLoader): Iterable dataset containing a list of (input_batch, expected_outputs) 
            batching_maxSize (int): batching_maxSize field for model.json
        """
        #self.export_to_krylov(validation_set) # Saves model and model.json to krylov, disabled for now
        self.validation_set_size = len(validation_set.dataset)
        self.batching_maxSize = batching_maxSize

        # Retina Results
        retina_ip = retina.start_inference_server() # Not sure yet if we need to wait here after starting the server before running infer()
        val_outputs_from_inference = retina.infer(retina_ip, validation_set, self.model_name, self.model_version)
        retina.close_inference_server() # Only close when validation is done

        # Training Results
        val_outputs_from_training = self.validate_trained_model(validation_set)

        # Compare Results
        results = self.compare_outputs(val_outputs_from_training, val_outputs_from_inference, difference_threshold)

        return results

    def export_to_krylov(self, validation_set):
        """ Saves traced model file and generated model.json to $KRYLOV_DATA_DIR/$KRYLOV_PRINCIPAL/ReVal/models/<model_name>/.
        Args:
            validation_set (dataLoader): Iterable dataset containing a list of (input_batch, expected_outputs) 
        """
        for data, target in validation_set:
            exampleInput = data
            break
        traced_model = torch.jit.trace(self.model, exampleInput)
        traced_model_directory = Util.get_model_folder_path(self.model_name)
        
        if not os.path.exists(traced_model_directory):
            os.makedirs(traced_model_directory)
        
        torch.jit.save(os.path.join(traced_model_directory, self.model_file_name))

        # Generate and save model.json file
        input_info = self.get_input_info("input", validation_set)
        output_info = self.get_output_info("output", validation_set)
        self.generate_model_json(input_info, output_info)

    def validate_trained_model(self, validation_set):
        """ Tests model object with the valdiation set data
        Args:
            validation_set (dataLoader): Iterable dataset containing a list of (input_batch, expected_outputs) 
        Returns:
            val_outputs_from_training (List of model outputs): Contains a list of output batches
        """
        val_outputs_from_training = []
        test_loss = 0
        correct = 0
        bar = Bar("Testing on Trained Model:", suffix='%(percent)d%% - %(eta)ds')
        for count, (input_batch, expected_outputs) in enumerate(validation_set):
            with torch.no_grad():
                output_batch = self.model(input_batch)
                val_outputs_from_training.append(output_batch.tolist())

                test_loss += F.nll_loss(output_batch, expected_outputs, reduction='sum')  # Sum up batch loss
                pred = output_batch.data.max(1, keepdim=True)[1]  # Get the index of the max log-probability
                correct += pred.eq(expected_outputs.data.view_as(pred)).long().cpu().sum()
            bar.next()
        bar.finish()

        test_loss /= self.validation_set_size
        print('\tAccuracy: {}/{} ({:.0f}%), Average loss: {:.4f}\n'.format(
            correct, self.validation_set_size,
            100. * correct / self.validation_set_size, test_loss))

        return val_outputs_from_training

    def compare_outputs(self, val_outputs_from_training, val_outputs_from_inference, difference_threshold):
        """ Compare training validation outputs with inference validation outputs (NOT TESTED)
        Args:
            val_outputs_from_training (List): List of outputs produced by model(input)
            val_outputs_from_inference (List): List of outputs produced by inference on the model
            difference_threshold (int): Threshold to determine whether a difference is significant (Typically 1e2 to 1e5)
        Returns:
            total_differences_between_models (int): All differences deemed significant by difference threshold
        """
        total_differences_between_models = 0
        under_threshold_differences = []
        under_threshold_indexes = []
        over_threshold_differences = []
        over_threshold_indexes = []
        largest_diff = difference_threshold
        for batch_count, (training_batch, inference_batch) in enumerate(zip(val_outputs_from_training, val_outputs_from_inference)):
            batch_differences = 0
            for individual_count, (training_output, inference_output) in enumerate(zip(training_batch, inference_batch)):
                difference_array = np.array(training_output) - np.array(inference_output)
                if abs(np.linalg.norm(difference_array)) > difference_threshold:
                    batch_differences += 1
                    if abs(np.linalg.norm(difference_array)) > largest_diff:
                        largest_diff = abs(np.linalg.norm(difference_array))
                        largest_diff_info = (batch_count * len(training_batch) + individual_count, training_output, inference_output)
                    over_threshold_differences.append(abs(np.linalg.norm(difference_array)))
                    over_threshold_indexes.append(batch_count * len(training_batch) + individual_count)
                else:                     
                    under_threshold_differences.append(abs(np.linalg.norm(difference_array)))
                    under_threshold_indexes.append(batch_count * len(training_batch) + individual_count)

            total_differences_between_models += batch_differences

        print("Comparison between trained model and hosted model:")
        print("\t{:.2f}% of the validation data had discrepencies greater than {}".format(
            100. * total_differences_between_models / self.validation_set_size,
            difference_threshold))
        print("\t{} differences / {} total data points".format(
            total_differences_between_models,
            self.validation_set_size))

        if largest_diff > difference_threshold:
            print("\tLargest Discrepency: {} (Index: {})".format("{:.2e}".format(
                decimal.Decimal(largest_diff)),
                largest_diff_info[0]))

        pyplot.yscale("log")
        pyplot.title("Differences Between Training and Inference Outputs")
        pyplot.xlabel("Index of Data in Validation Set")
        pyplot.ylabel("Difference")

        pyplot.axhline(y=1e-3, c='gray', linestyle='--')
        pyplot.axhline(y=1e-4, c='gray', linestyle='--')
        pyplot.axhline(y=1e-5, c='gray', linestyle='--')
        pyplot.axhline(y=1e-6, c='gray', linestyle='--')
        pyplot.axhline(y=1e-7, c='gray', linestyle='--')
        pyplot.axhline(y=difference_threshold, c='firebrick', linestyle='--')

        pyplot.scatter(under_threshold_indexes, under_threshold_differences, c='blue')
        pyplot.scatter(over_threshold_indexes, over_threshold_differences, c='red')
        pyplot.show()

        return total_differences_between_models

    def generate_model_json(self, input_info, output_info):
        """ Writes model.json to current directory
        Args:
            input_info (str[3]): (inputName, inputDataType, inputSize)
            output_info (str[3]): (outputName, outputDataType, outputSize)
        """
        backend_name, backend_version, backend_platform, backend_format = self.backend_processing()
        batching_strategy = "bufferTimeout"
        batching_timeoutMillis = 4

        # Identity
        data = {'name': self.model_name, 'version': self.model_version}
        
        # Backend
        data['backend'] = {'name': backend_name, 'version': backend_version}
        if backend_platform != "" or backend_format != "": data['backend']['params'] = {}
        if backend_platform != "": data['backend']['params'].update({'platform': backend_platform})
        if backend_format != "": data['backend']['params'].update({'format': backend_format})
        data['backend']['files'] = {'model': self.model_file_name}
        
        # Batching
        data['batching'] = {'strategy': batching_strategy}
        if batching_strategy != "passthrough": data['batching']['params'] = {}
        if self.batching_maxSize != "": data['batching']['params'].update({'maxSize': self.batching_maxSize})
        if batching_timeoutMillis != "": data['batching']['params'].update({'timeoutMillis': batching_timeoutMillis})
       
        # Inputs
        data['inputs'] = []
        data['inputs'].append({'name': input_info[0]+'__0', 'displayName': input_info[0], 'dataType': input_info[1]})
        if input_info[1] == "FLOAT": data['inputs'][0].update({'rawInput': {"DOUBLE": input_info[2]}})
        data['inputs'][0].update({'shape': input_info[2]})
        
        # Outputs
        data['outputs'] = []
        data['outputs'].append({'name': output_info[0]+'__0', 'displayName': output_info[0], 'dataType': output_info[1], 'shape': output_info[2]})
        
        # Write to file
        with open(Util.get_model_json_path(self.model_name), 'w') as outfile:
            json.dump(data, outfile, indent=2)

    def backend_processing(self):
        """ Determines correct backend information for model.json
        Args:
            model_file_extension (str): File extension characters (ex. 'pb', 'pt', 'onnx', etc)
            backend_type (str): Backend type required to see if using test, triton, or tensorFlow
        Returns: 
            (str[4]): (backend_name, backend_version, backend_platform, and backend_format)
        """
        model_file_extension = self.model_file_name.split('.')[1]
        backend_name = ""
        backend_version = "1"
        backend_platform = ""
        backend_format = ""

        if self.backend_type == "triton":
            backend_version = "20.10"
            if model_file_extension == "pb":
                backend_name = "triton"
                backend_platform = "tensorflow"
                backend_format = "savedModel"
            elif model_file_extension == "graphdef":
                backend_name = "triton"
                backend_platform = "tensorflow"
                backend_format = "frozenGraph"
            elif model_file_extension == "pt":
                backend_name = "triton"
                backend_platform = "pytorch"
            elif model_file_extension == "plan":
                backend_name = "triton"
                backend_platform = "tensorrt"
            elif model_file_extension == "onnx":
                backend_name = "triton"
                backend_platform = "onnx"
        elif self.backend_type == "tensorFlow":
            if model_file_extension == "pb":
                backend_name = "tensorflow"
                backend_format = "savedModel"
            elif model_file_extension == "graphdef":
                backend_name = "tensorflow"
                backend_format = "frozenGraph"
        elif self.backend_type == "test":
            return "test", "1", "", ""
        else:
            raise Exception("Unexpected backend_type error")

        return backend_name, backend_version, backend_platform, backend_format

    def get_input_info(self, inputName, dataLoader):
        """ Grabs the shape and data type of a model input (TODO - Test and Improve for other datasets)
        Args:
            inputName (str): Name of input in model.json
            dataLoader (torch.Dataloader): dataLoader[0] is assumed to be in [input_tensor, expected_output] format
        Returns: 
            (inputName, inputDataType, inputSize)
        """
        for data, target in dataLoader:
            exampleInput = data[0]
            break
        # Converts tensor.dtype to actual dataType (https://pytorch.org/docs/stable/tensors.html)
        inputDataType = re.sub(r'[0-9]', '', str(exampleInput.dtype).replace('torch.', '').replace('Tensor', '').upper())
        inputSize = list(exampleInput.shape)
        return inputName, inputDataType, inputSize
    
    def get_output_info(self, outputName, dataLoader):
        """ Grabs the shape and data type of a model output (TODO - Test and Improve for other datasets)
        Args:
            outputName (str): Name of output in model.json
            dataLoader (torch.Dataloader): dataLoader[0] is assumed to be in [input_tensor, expected_output] format
        Returns: 
            (outputName, outputDataType, outputSize) 
        """
        for data, target in dataLoader:
            with torch.no_grad():
                exampleOutput = self.model(data)[0]
            break
        # Converts tensor.dtype to actual dataType (https://pytorch.org/docs/stable/tensors.html)
        outputDataType = re.sub(r'[0-9]', '', str(exampleOutput.dtype).replace('torch.', '').replace('Tensor', '').upper())
        outputSize = list(exampleOutput.shape)
        return outputName, outputDataType, outputSize




