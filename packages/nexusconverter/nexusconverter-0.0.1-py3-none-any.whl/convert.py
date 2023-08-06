"""
作者：郭帅
邮箱：gs0801@foxmail.com
更新日期：2021/07/09
TODO:
  1. 处理非 __init__ 内的计算；
  2. 处理参数初始化；
"""
import re
import sys
try:
    from parse import parse
except ImportError:
    print("You should install parse first.\n  $ pip install --user parse")
    sys.exit(1)
import torch


# PyTorch module 到 Nexus Symbol 的映射
PT2NX = {
    "Conv2d": "Convolution",
    "MaxPool2d": "Pooling",
    "Linear": "FullyConnected",
    "Dropout": "Dropout",
    "ReLU": "Relu",
    "Flatten": "Flatten",
    "Sigmoid": "Sigmoid",
    "Tanh": "Tanh",
    "Softmax": "Softmax"
}

def toNexusCode(model, data):
    traced_model = torch.jit.trace(model, data)
    m = {}
    program = []
    arg_idx = 0
    content = str(traced_model.graph)
    content = re.sub(r"#.*\n", "\n", content)
    r = parse("graph({arguments}):{body}", content)
    """ 首先处理图的输入 """
    for arg in r["arguments"].split("\n"):
        parsed = parse("{tag} : {obj}", arg.strip())
        if parsed["obj"].startswith("_"): continue
        obj_parsed = parse("Float({shape_str}, strides={_})", parsed["obj"])
        arg = {}
        arg["name"] = f"data{arg_idx}"
        arg_idx += 1
        arg["shape"] = [int(x) for x in obj_parsed["shape_str"].split(", ")]
        m[parsed["tag"]] = arg
        program.append(f'auto {arg["name"]} = Symbol::Variable("{arg["name"]}");')
    """ 然后处理图的内部 (body) """
    for line in r["body"].split("\n"):
        line = line.strip()
        if len(line) == 0: continue
        if line.startswith("return"):
            m["return"] = parse("return ({tag})", line)["tag"]
            break
        parsed = parse("{tag} : {lhs} = {rhs}", line)
        if parsed["lhs"].startswith("_"):
            layer = {}
            layer["symbol"] = PT2NX[parsed["lhs"].split(".")[-1]]
            layer["name"] = parse('prim::GetAttr[name="{name}"]({_})', parsed["rhs"])["name"]
            if layer["symbol"] == "Convolution":
                layer["kernel"] = list(getattr(model, layer["name"]).kernel_size)
                layer["filters"] = getattr(model, layer["name"]).out_channels
                layer["stride"] = list(getattr(model, layer["name"]).stride)
                layer["padding"] = list(getattr(model, layer["name"]).padding)
                layer["dilation"] = list(getattr(model, layer["name"]).dilation)
                layer["bias"] = getattr(model, layer["name"]).bias
            elif layer["symbol"] == "FullyConnected":
                layer["out_features"] = getattr(model, layer["name"]).out_features
                layer["bias"] = getattr(model, layer["name"]).bias
            elif layer["symbol"] == "Pooling":
                layer["kernel"] = getattr(model, layer["name"]).kernel_size
                layer["stride"] = getattr(model, layer["name"]).stride
                layer["padding"] = getattr(model, layer["name"]).padding
            elif layer["symbol"] == "Dropout":
                layer["p"] = getattr(model, layer["name"]).p
            m[parsed["tag"]] = layer
        elif parsed["lhs"] == "Tensor":
            layer_parsed = parse('prim::CallMethod[name="forward"]({layer_tag}, {input_tag})', parsed["rhs"])
            layer_tag = layer_parsed["layer_tag"]
            input_tag = layer_parsed["input_tag"]
            layer = m[layer_tag]
            m[parsed["tag"]] = {"name": layer["name"]}
            # if input_tag not in m: continue
            input = m[input_tag]
            stmt = f'auto {layer["name"]} = {layer["symbol"]}("{layer["name"]}", {input["name"]}'
            if layer["symbol"] == "Convolution":
                stmt += ", {" + ", ".join([str(x) for x in layer["kernel"]]) + "}"
                stmt += f', {layer["filters"]}'
                stmt += ", true" if layer["bias"] else ", false"
                stmt += ", {" + ", ".join([str(x) for x in layer["stride"]]) + "}"
                stmt += ", {" + ", ".join([str(x) for x in layer["dilation"]]) + "}"
                stmt += ", {" + ", ".join([str(x) for x in layer["padding"]]) + "}"
            elif layer["symbol"] == "FullyConnected":
                stmt += f', {layer["out_features"]}'
                stmt += ", true" if layer["bias"] else ", false"
                stmt += ", true"
            elif layer["symbol"] == "Pooling":
                stmt += f', {layer["kernel"]}, {layer["stride"]}, {layer["padding"]}'
            elif layer["symbol"] == "Dropout":
                stmt += f', {layer["p"]}'
            program.append(stmt + ");")

    return "\n".join(program)
