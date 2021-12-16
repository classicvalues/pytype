"""Tests for typing.TypedDict."""

from pytype.tests import test_base


class TypedDictTest(test_base.BaseTest):
  """Tests for typing.TypedDict."""

  def test_key_error(self):
    err = self.CheckWithErrors("""
      from typing_extensions import TypedDict
      class A(TypedDict):
        x: int
        y: str
      a = A()
      a["z"] = 10  # typed-dict-error[e1]
      a[10] = 10  # typed-dict-error[e2]
      b = a["z"]  # typed-dict-error
      del a["z"]  # typed-dict-error
    """)
    self.assertErrorSequences(err, {
        "e1": ["TypedDict A", "key z"],
        "e2": ["TypedDict A", "requires all keys", "strings"],
    })

  def test_value_error(self):
    err = self.CheckWithErrors("""
      from typing_extensions import TypedDict
      class A(TypedDict):
        x: int
        y: str
      a = A()
      a["x"] = "10"  # annotation-type-mismatch[e]
    """)
    self.assertErrorSequences(err, {"e": [
        "Type annotation", "key x", "TypedDict A",
        "Annotation: int", "Assignment: str"
    ]})

  def test_union_type(self):
    err = self.CheckWithErrors("""
      from typing_extensions import TypedDict
      from typing import Union
      class A(TypedDict):
        x: Union[int, str]
        y: Union[int, str]
      a = A()
      a["x"] = "10"
      a["y"] = []  # annotation-type-mismatch[e]
    """)
    self.assertErrorSequences(err, {"e": [
        "Type annotation", "key y", "TypedDict A",
        "Annotation: Union[int, str]", "Assignment: List[nothing]"
    ]})

if __name__ == "__main__":
  test_base.main()
