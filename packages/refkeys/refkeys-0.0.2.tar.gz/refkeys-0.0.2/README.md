# Refkeys: A secure way for sharing secret (key).
#### Author & Developer: [Ravin Kumar](https://mr-ravin.github.io)
This repository contains a tool for secret-sharing among two parties.

For example, lets say two parties A and B want to share a secret_key, such that only if they both agree than only they should be able to get the secret.
Our software generates 3 individual keys, one for each party, and one for the mediator. When these keys are combined then only the secret_key can be revealed.

#### Advantage of our system:
- Even though the same secret is shared among G1={a,b,c} and G2={x,y,z}. The beauty of refkeys is that, even if some member of a group tries to contact other group members to generate the secret key, it can not be generated.
- Only when all parties of G1 agrees than only they can generate the secret_key.

#### Demonstration for generating individual keys:
```python
import refkeys
key=refkeys.get_keys("secure_key_passed_here")
person1_key=key[0]
person2_key=key[1]
mediator_key=key[2]
## note: person1_key,person2_key,mediator_key are of type-list.
```

#### Demonstration for generating individual filekeys:
```python
import refkeys
refkeys.get_keyfiles("secure_key_passed_here","person1_name","person2_name","mediator_name",path="./")
## note: names should be distinct, and mediator name is not mandatory.
```



#### Demonstration for generating secret key using individual keys:
```python
import refkeys
....
secret_key=refkeys.combine_keys(person1_key,person2_key,mediator_key)
## note: person1_key,person2_key,mediator_key are of type-list.
```


#### Demonstration for generating secret key using filekeys:
```python
import refkeys
....
secret_key=refkeys.combine_keyfiles(person1_key,person2_key,mediator_key)
## note: names should be distinct, and mediator name is not mandatory.
```

#### Installation using pip:
```python
pip install refkeys
```

```python
Copyright (c) 2019 Ravin Kumar
Website: https://mr-ravin.github.io

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation 
files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, 
modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the 
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the 
Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE 
WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR 
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, 
ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
```

