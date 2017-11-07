import os
import sys
import importlib

import argparse

import gen

class DummyTypeConverterCommon(gen.TypeConverter):
    def __init__(self, type, arg_storage_type=None, bound_name=None, rval_storage_type=None, needs_c_storage_class=False):
        super().__init__(type, arg_storage_type, bound_name, rval_storage_type, needs_c_storage_class)

    def get_type_api(self, module_name):
        return ''

    def to_c_call(self, in_var, out_var_p):
        return ''

    def from_c_call(self, out_var, expr, ownership):
        return ''

    def check_call(self, in_var):
        return ''

    def get_type_glue(self, gen, module_name):
        return ''

class APIGenerator(gen.FABGen):
    default_ptr_converter = DummyTypeConverterCommon
    default_class_converter = DummyTypeConverterCommon

    def __init__(self):
        super().__init__()
        self.check_self_type_in_ops = True

    def get_language(self):
        return "CPython" # little hack :/

    def output_includes(self):
        pass

    def start(self, module_name):
        super().start(module_name)

    def set_error(self, type, reason):
        return ''

    def get_self(self, ctx):
        return '1'  # always first arg

    def get_arg(self, i, ctx):
        return str(i)

    def open_proxy(self, name, max_arg_count, ctx):
        return ''

    def close_proxy(self, ctx):
        return ''

    def proxy_call_error(self, msg, ctx):
        return ''

    def return_void_from_c(self):
        return ''

    def rval_from_c_ptr(self, conv, out_var, expr, ownership):
        return ''

    def commit_rvals(self, rvals, ctx='default'):
        return ''

    def output_binding_api(self):
        return '', ''

    def extract_method(self, classname, method, static=False, name=None, bound_name=None):
        xml = ""
        if bound_name is None:
            bound_name = method['bound_name']
        if name is None:
            name = bound_name
        protos = self._build_protos(method['protos'])
        for proto in protos:
            retval = 'val'
            if proto['rval']['conv']:
                retval = proto['rval']['conv'].bound_name
            xml += '<function name="%s" returns="%s" uid="%s_%s"' % (name, retval, classname, bound_name)
            if static: xml += ' static="1"'
            if len(proto['args']):
                xml += '>\n'
                for argin in proto['argsin']:
                    xml += '<parm name="%s" type="%s"/>\n' % (argin['carg'].name, argin['conv'].bound_name)
                if 'arg_out' in proto['features']:
                    i = 0
                    for arg in proto['args']:
                        if arg['carg'].name in proto['features']['arg_out']:
                            xml += '<param name="OUTPUT%d" type="%s"/>\n' % (i, arg['conv'].bound_name)
                            i += 1
                xml += '</function>\n'
            else:
                xml += '/>\n'
        return xml

    def output_xml_api(self):
        xml = '<?xml version="1.0" ?>\n<api>\n'
        for conv in self._bound_types:
            if conv.nobind:
                pass
            
            if conv.methods or conv.members:
                xml += '<class name="%s" uid="%s">\n' % (conv.bound_name, conv.bound_name)
                # base
                for base in conv._bases:
                    xml += '<inherits uid="%s"/>\n' % base.bound_name
                # static members
                for member in conv.static_members:
                    xml += '<variable name="%s" static="1" type="%s"/>\n' % (member['name'], self.select_ctype_conv(member['ctype']).bound_name)
                # members
                for member in conv.members:
                    xml += '<variable name="%s" type="%s"/>\n' % (member['name'], self.select_ctype_conv(member['ctype']).bound_name)
                # constructors
                if conv.constructor:
                    xml += self.extract_method(conv.bound_name, conv.constructor, bound_name="Constructor")
                # arithmetic operators
                for arithmetic in conv.arithmetic_ops:
                    bound_name = 'operator_' + gen.get_clean_symbol_name(arithmetic['op'])
                    xml += self.extract_method(conv.bound_name, arithmetic, name='operator'+arithmetic['op'], bound_name=bound_name)
                # comparison_ops
                for comparison in conv.comparison_ops:
                    bound_name = 'operator_' + gen.get_clean_symbol_name(comparison['op'])
                    xml += self.extract_method(conv.bound_name, comparison, name='operator'+comparison['op'], bound_name=bound_name)
                # static methods
                for method in conv.static_methods:
                    xml += self.extract_method(conv.bound_name, method, static=True)
                # methods
                for method in conv.methods:
                    xml += self.extract_method(conv.bound_name, method)
                xml += '</class>\n'
        
        # enum
        for bound_name, enum in self._enums.items():
            xml += '<enum global="1" name="%s" uid="%s">\n' % (bound_name, bound_name)
            for name, value in enum.items():
                xml += '<entry name="%s"/>\n' % name
            xml +=  '</enum>\n'
        xml += '</api>\n'
        return xml

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='API generation script')
    parser.add_argument("script", nargs=1)
    parser.add_argument('--out', help='Path to output generated files', required=True)
    args = parser.parse_args()

    # load binding script
    split = os.path.split(args.script[0])
    path = split[0]
    mod = os.path.splitext(split[1])[0]

    sys.path.append(path)
    script = importlib.import_module(mod)

    api_gen = APIGenerator()
    script.bind(api_gen)
    xml = api_gen.output_xml_api()
    api_path = os.path.join(args.out, 'api.xml')
    with open(api_path, mode='w', encoding='utf-8') as f:
        f.write(xml)
