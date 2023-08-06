# Assertions

<!--BEGIN STABILITY BANNER-->---


![cdk-constructs: Experimental](https://img.shields.io/badge/cdk--constructs-experimental-important.svg?style=for-the-badge)

> The APIs of higher level constructs in this module are experimental and under active development.
> They are subject to non-backward compatible changes or removal in any future version. These are
> not subject to the [Semantic Versioning](https://semver.org/) model and breaking changes will be
> announced in the release notes. This means that while you may use them, you may need to update
> your source code when upgrading to a newer version of this package.

---
<!--END STABILITY BANNER-->

Functions for writing test asserting against CDK applications, with focus on CloudFormation templates.

The `TemplateAssertions` class includes a set of methods for writing assertions against CloudFormation templates. Use one of the `TemplateAssertions.fromXxx()` static methods to create an instance of this class.

To create `TemplateAssertions` from CDK stack, start off with:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
from aws_cdk.core import Stack
from aws_cdk.assertions import TemplateAssertions

stack = Stack(...)
assert = TemplateAssertions.from_stack(stack)
```

Alternatively, assertions can be run on an existing CloudFormation template -

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
template = fs.read_file_sync("/path/to/template/file")
assert = TemplateAssertions.from_string(template)
```

## Full Template Match

The simplest assertion would be to assert that the template matches a given
template.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
assert.template_matches(
    Resources={
        "Type": "Foo::Bar",
        "Properties": {
            "Baz": "Qux"
        }
    }
)
```

## Counting Resources

This module allows asserting the number of resources of a specific type found
in a template.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
assert.resource_count_is("Foo::Bar", 2)
```

## Resource Matching

Beyond resource counting, the module also allows asserting that a resource with
specific properties are present.

The following code asserts that the `Properties` section of a resource of type
`Foo::Bar` contains the specified properties -

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
assert.has_resource_properties("Foo::Bar",
    Foo="Bar",
    Baz=5,
    Qux=["Waldo", "Fred"]
)
```

Alternatively, if you would like to assert the entire resource definition, you
can use the `hasResource()` API.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
assert.has_resource("Foo::Bar",
    Properties={"Foo": "Bar"},
    DependsOn=["Waldo", "Fred"]
)
```

By default, the `hasResource()` and `hasResourceProperties()` APIs perform deep
partial object matching. This behavior can be configured using matchers.
See subsequent section on [special matchers](#special-matchers).

## Special Matchers

The expectation provided to the `hasResourceXXX()` methods, besides carrying
literal values, as seen in the above examples, can also have special matchers
encoded.
They are available as part of the `Match` class.

### Object Matchers

The `Match.objectLike()` API can be used to assert that the target is a superset
object of the provided pattern.
This API will perform a deep partial match on the target.
Deep partial matching is where objects are matched partially recursively. At each
level, the list of keys in the target is a subset of the provided pattern.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
# Given a template -
# {
#   "Resources": {
#     "MyBar": {
#       "Type": "Foo::Bar",
#       "Properties": {
#         "Fred": {
#           "Wobble": "Flob",
#           "Bob": "Cat"
#         }
#       }
#     }
#   }
# }

# The following will NOT throw an assertion error
assert.has_resource_properties("Foo::Bar",
    Fred=Match.object_like(
        Wobble="Flob"
    )
)

# The following will throw an assertion error
assert.has_resource_properties("Foo::Bar",
    Fred=Match.object_like(
        Brew="Coffee"
    )
)
```

The `Match.objectEquals()` API can be used to assert a target as a deep exact
match.

In addition, the `Match.absentProperty()` can be used to specify that a specific
property should not exist on the target. This can be used within `Match.objectLike()`
or outside of any matchers.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
# Given a template -
# {
#   "Resources": {
#     "MyBar": {
#       "Type": "Foo::Bar",
#       "Properties": {
#         "Fred": {
#           "Wobble": "Flob",
#         }
#       }
#     }
#   }
# }

# The following will NOT throw an assertion error
assert.has_resource_properties("Foo::Bar",
    Fred=Match.object_like(
        Bob=Match.absent_property()
    )
)

# The following will throw an assertion error
assert.has_resource_properties("Foo::Bar",
    Fred=Match.object_like(
        Wobble=Match.absent_property()
    )
)
```

### Array Matchers

The `Match.arrayWith()` API can be used to assert that the target is equal to or a subset
of the provided pattern array.
This API will perform subset match on the target.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
# Given a template -
# {
#   "Resources": {
#     "MyBar": {
#       "Type": "Foo::Bar",
#       "Properties": {
#         "Fred": ["Flob", "Cat"]
#       }
#     }
#   }
# }

# The following will NOT throw an assertion error
assert.has_resource_properties("Foo::Bar",
    Fred=Match.array_with(["Flob"])
)

# The following will throw an assertion error
assert.has_resource_properties("Foo::Bar", Match.object_like(
    Fred=Match.array_with(["Wobble"])
));
```

*Note:* The list of items in the pattern array should be in order as they appear in the
target array. Out of order will be recorded as a match failure.

Alternatively, the `Match.arrayEquals()` API can be used to assert that the target is
exactly equal to the pattern array.

## Strongly typed languages

Some of the APIs documented above, such as `templateMatches()` and
`hasResourceProperties()` accept fluently an arbitrary JSON (like) structure
its parameter.
This fluency is available only in dynamically typed languages like javascript
and Python.

For strongly typed languages, like Java, you can achieve similar fluency using
any popular JSON deserializer. The following Java example uses `Gson` -

```java
// In Java, using text blocks and Gson
import com.google.gson.Gson;

String json = """
  {
    "Foo": "Bar",
    "Baz": 5,
    "Qux": [ "Waldo", "Fred" ],
  } """;

Map expected = new Gson().fromJson(json, Map.class);
assert.hasResourceProperties("Foo::Bar", expected);
```
