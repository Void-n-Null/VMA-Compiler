import contextlib
import json

class ParameterExtractor:
    @staticmethod
    def extract_parameters(parameters_str: str) -> list:
        param_dict = ParameterExtractor._extract_dict(parameters_str)
        parameters_str = parameters_str.replace(str(param_dict), 'DICTPLACEHOLDER')

        result = [
            int(param) if param.isdigit() else
            float(param) if param.replace('.', '', 1).isdigit() else
            param.strip('"').strip("'") if param not in ['DICTPLACEHOLDER'] else param_dict
            for param in parameters_str.split(',')
        ]

        # Turn dict strings into dicts
        for i, parameter in enumerate(result):
            with contextlib.suppress(Exception):
                result[i] = json.loads(parameter)
        return result

    @staticmethod
    def _extract_dict(s: str) -> dict:
        start, end = s.find('{'), s.rfind('}')
        if start != -1 and end != -1:
            try:
                return eval(s[start:end + 1])
            except Exception:
                return {}
        return {}