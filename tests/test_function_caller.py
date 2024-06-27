import unittest
from easy_fnc.function_caller import FunctionCallingEngine, create_functions_metadata
from easy_fnc.schemas import FunctionMetadata, FunctionReturn, ModelResponse, FunctionCall

def addition_function(x: int, y: int) -> int:
    """Test function that adds two numbers."""
    return x + y

class TestFunctionCallingEngine(unittest.TestCase):
    def setUp(self):
        self.engine = FunctionCallingEngine(auto_load_core_utils=False)
        self.engine.functions['addition_function'] = addition_function

    def test_create_functions_metadata(self):
        metadata = create_functions_metadata(self.engine.functions)
        self.assertIsInstance(metadata, list)
        self.assertIsInstance(metadata[0], FunctionMetadata)
        self.assertEqual(metadata[0].name, 'addition_function')
        self.assertEqual(metadata[0].description, 'Test function that adds two numbers.')
        self.assertEqual(metadata[0].parameters['properties'], {'x': 'int', 'y': 'int'})
        self.assertEqual(metadata[0].returns, [FunctionReturn(name='addition_function_output', type='int')])

    def test_parse_model_response(self):
        raw_response = """<|thoughts|>
The user wants to add two numbers. I'll use the addition_function for this.
<|end_thoughts|>
<|function_calls|>
[
    {
        "name": "addition_function",
        "kwargs": {"x": 5, "y": 3},
        "returns": ["result"]
    }
]
<|end_function_calls|>
"""
        response = self.engine.parse_model_response(raw_response)
        self.assertIsInstance(response, ModelResponse)
        self.assertEqual(len(response.function_calls), 1)
        self.assertEqual(response.function_calls[0].name, 'addition_function')
        self.assertEqual(response.function_calls[0].kwargs, {'x': 5, 'y': 3})
        self.assertEqual(response.function_calls[0].returns, ['result'])

    def test_call_functions(self):
        function_calls = [
            FunctionCall(name='addition_function', kwargs={'x': 5, 'y': 3}, returns=['result'])
        ]
        outputs = self.engine.call_functions(function_calls)
        self.assertEqual(outputs['result'], 8)

if __name__ == '__main__':
    unittest.main()