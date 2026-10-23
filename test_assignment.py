import ast
import importlib
import inspect
import textwrap

import pytest

import assignment


@pytest.fixture
def s():
    return importlib.reload(assignment)


def calls_in(function):
    tree = ast.parse(textwrap.dedent(inspect.getsource(function)))
    names = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name):
                names.append(node.func.id)
            if isinstance(node.func, ast.Attribute):
                names.append("." + node.func.attr)
    return names


def check_no_list_methods(function):
    for name in calls_in(function):
        if name in [".append", ".pop", ".insert", ".remove", ".extend", ".clear"]:
            pytest.fail(
                function.__name__ + "() uses " + name + "(). "
                "Change TopOfStack and use Stack[TopOfStack] instead."
            )


def test1_initial_stack(s):
    assert s.Stack == ["", "", "", "", "", "", "", ""]
    assert s.TopOfStack == -1


def test1_push(s):
    assert s.Push("I") == True
    assert s.TopOfStack == 0
    assert s.Stack[0] == "I"
    assert s.Push("love") == True
    assert s.TopOfStack == 1
    assert s.Stack[1] == "love"


def test1_push_when_full(s):
    for word in ["a", "b", "c", "d", "e", "f", "g", "h"]:
        assert s.Push(word) == True
    assert s.TopOfStack == 7
    assert s.Push("i") == False
    assert s.TopOfStack == 7
    assert s.Stack == ["a", "b", "c", "d", "e", "f", "g", "h"]


def test1_pop(s):
    s.Push("I")
    s.Push("love")
    s.Push("Python")
    assert s.Pop() == "Python"
    assert s.TopOfStack == 1
    assert s.Pop() == "love"
    assert s.Pop() == "I"
    assert s.TopOfStack == -1


def test1_pop_when_empty(s):
    assert s.Pop() == ""
    assert s.TopOfStack == -1
    s.Push("hi")
    s.Pop()
    assert s.Pop() == ""
    assert s.TopOfStack == -1


def test1_uses_top_of_stack(s):
    check_no_list_methods(s.Push)
    check_no_list_methods(s.Pop)
    for x in range(10):
        s.Push("w" + str(x))
    for x in range(10):
        s.Pop()
    assert len(s.Stack) == 8


def test1_get_text(s):
    assert s.GetText() == ""
    s.Push("I")
    assert s.GetText() == "I"
    s.Push("love")
    s.Push("Python")
    assert s.GetText() == "I love Python"
    s.Pop()
    assert s.GetText() == "I love"
    s.Push("cats")
    assert s.GetText() == "I love cats"


def test1_get_text_keeps_stack(s):
    s.Push("I")
    s.Push("love")
    s.Push("Python")
    s.GetText()
    s.GetText()
    assert s.TopOfStack == 2
    assert s.Pop() == "Python"


@pytest.mark.parametrize("number, expected", [
    [5, "101"],
    [10, "1010"],
    [1, "1"],
    [2, "10"],
    [0, "0"],
    [128, "10000000"],
    [255, "11111111"],
    [100, "1100100"],
])
def test2_binary(s, number, expected):
    assert s.DecimalToBinary(number) == expected


def test2_stack_empty_after(s):
    assert s.DecimalToBinary(13) == "1101"
    assert s.TopOfStack == -1


def test2_starts_with_empty_stack(s):
    s.Push("x")
    s.Push("y")
    assert s.DecimalToBinary(5) == "101"
    s.Push("1")
    assert s.DecimalToBinary(6) == "110"


def test2_uses_the_stack(s):
    names = calls_in(s.DecimalToBinary)
    for banned in ["bin", "format", ".format"]:
        if banned in names:
            pytest.fail("DecimalToBinary() uses " + banned + "(). Use the stack instead.")
    assert "Push" in names, "DecimalToBinary() must call Push()."
    assert "Pop" in names, "DecimalToBinary() must call Pop()."
