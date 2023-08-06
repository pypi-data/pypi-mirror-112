from __future__ import annotations
from typing import Any, Union, List

# __all__ = ["Bit", "Nibble", "Byte", "ByteLike", "Word", "DoubleWord", "QuadWord"]

# ERRORS:
# class ByteError(Exception):
# 	__module__ = Exception.__module__
# 	def __init__(self, *args, **kwargs):
# 		Exception.__init__(self, *args, **kwargs)
# 		self.__class__.__name__ = "ByteError"

def _int_to_bits(value: int, length: int = False) -> List[int]:
	"""convert a decimal integer to a list of bits as short as possible"""
	value = abs(int(value))

	if value == 0: return [0]*length if length else [0]
	# if value == 1: return [1]

	bits: List[int] = []

	while value:
		bits.append(value%2)
		value //= 2
	
	if length:
		orlen = len(bits)
		if orlen < length:
			for _ in range(length-orlen):
				bits.append(0)
		if orlen > length:
			bits = bits[:length-1]

	bits.reverse()
	return bits

def _bits_to_int(bits: List[int]) -> int:
	value = 0
	for bit in bits:#[1:]:
		value = value * 2 + bit
	return value

def _bits_to_hex(bits: List[int]) -> str:
	if len(bits) == 0:
		pad = 4
	elif len(bits) % 4 == 0:
		pad = 0
	else:
		pad = 4 - len(bits) % 4
	
	for _ in range(pad):
		bits.insert(0, 0)
	
	# turn bits list into nibbles
	nibbles = [bits[i * 4:(i + 1) * 4] for i in range((len(bits) + 4 - 1) // 4 )]
	hexstr = "0x"

	for nibble in nibbles:
		dec = _bits_to_int(nibble)
		if dec > 9:
			# print(dec-8)
			dec = 'abcdef'[dec-10]
		hexstr+= str(dec)

	return hexstr

class Bit:
	"""Class representing a single bit"""

	# FUNCTIONS
	def __init__(self, value: Any) -> Bit: # type: ignore
		# initializes a Bit instance
		self._value: bool = bool(value)

	def __str__(self) -> str: # type: ignore
		return str(int(bool(self._value)))

	def __len__(self) -> int: # type: ignore
		return 1

	def __repr__(self) -> str: # type: ignore
		return f"Bit({self._value})"
			
	def __bool__(self) -> bool: # type: ignore
		return bool(self._value)

	def __hash__(self) -> int: # type: ignore
		return hash(self._value)

	def __format__(self, format_spec: str) -> str: # type: ignore
		return f'Bit({self._value:{format_spec}})' 

	# def __dir__(self) -> Iterable[str]: # type: ignore
		# pass

	# BINARY OPERATORS
	def __add__(self, other: Any) -> Bit: # type: ignore
		otherbit = Bit(other)
		if not self._value:
			# self = 0, so whatever the other bit is it will be the result
			return otherbit
		elif otherbit._value:
			# self = 1, other = 1, return is 0
			return Bit(0)
		else:
			# self = 1, other = 0, return is 1
			return Bit(1)

	def __sub__(self, other: Any) -> Bit: # type: ignore
		otherbit = Bit(other)
		if not self._value:
			# self = 0, result is always 0
			return Bit(0)
		elif otherbit._value:
			# self = 1, other = 1, return 0
			return Bit(0)
		else:
			# self = 1, other = 0, return 1
			return Bit(1)
			
	def __mul__(self, other: Any) -> Bit: # type: ignore
		otherbit = Bit(other)
		if self._value and otherbit._value:
			# both 1, return 1
			return Bit(1)
		else:
			# all other cases are 0
			return Bit(0)

	def __truediv__(self, other: Any) -> Bit: # type: ignore
		raise NotImplementedError

	def __floordiv__(self, other: Any) -> Bit: # type: ignore
		raise NotImplementedError

	def __mod__(self, other: Any) -> Bit: # type: ignore
		raise NotImplementedError

	def __pow__(self, other: Any) -> Bit: # type: ignore
		raise NotImplementedError

	# ASSIGNMENT OPERATORS
	def __iadd__(self, other: Any) -> Bit: # type: ignore
		self = self.__add__(other)

	def __isub__(self, other: Any) -> Bit: # type: ignore
		self = self.__sub__(other)

	def __imul__(self, other: Any) -> Bit: # type: ignore
		self = self.__mul__(other)

	def __idiv__(self, other: Any) -> Bit: # type: ignore
		self = self.__div__(other)

	def __ifloordiv__(self, other: Any) -> Bit: # type: ignore
		self = self.__floordiv__(other)

	def __imod__(self, other: Any) -> Bit: # type: ignore
		self = self.__mod__(other)

	def __ipow__(self, other: Any) -> Bit: # type: ignore
		self = self.__pow__(other)

	# COMPARISON OPERATORS
	def __lt__(self, other: Any) -> bool: # type: ignore
		otherbit = Bit(other)
		return (int(self._value) < int(otherbit._value))

	def __gt__(self, other: Any) -> bool: # type: ignore
		otherbit = Bit(other)
		return (int(self._value) > int(otherbit._value))

	def __le__(self, other: Any) -> bool: # type: ignore
		otherbit = Bit(other)
		return (int(self._value) <= int(otherbit._value))

	def __ge__(self, other: Any) -> bool: # type: ignore
		otherbit = Bit(other)
		return (int(self._value) >= int(otherbit._value))

	def __eq__(self, other: Any) -> bool: # type: ignore
		otherbit = Bit(other)
		return (int(self._value) == int(otherbit._value))

	def __ne__(self, other: Any) -> bool: # type: ignore
		otherbit = Bit(other)
		return (int(self._value) != int(otherbit._value))

	# UNARY OPERATORS
	def __neg__(self) -> Bit: # type: ignore
		raise NotImplementedError

	def __pos__(self) -> Bit: # type: ignore
		raise NotImplementedError

	def __invert__(self) -> Bit: # type: ignore
		return Bit(not self._value)

class _MultipleBits:
	"""Class containing immutable amount of bits"""

	# FUNCTIONS
	def __init__(self, bits: List[Bit]) -> _MultipleBits: # type: ignore
		# initializes a _MultipleBits instance
		if not all(isinstance(x, Bit) for x in bits):
			raise ValueError("_MultipleBits takes a list of Bit instances")
		self._bits: List[Bit] = bits
		self._len: int = len(bits)
	
	def __str__(self) -> str: # type: ignore
		return ''.join(str(x) for x in self._bits)

	def __len__(self) -> int: # type: ignore
		return self._len

	def __repr__(self) -> str: # type: ignore
		return f"_MultipleBits({self._bits})"
	
	def __bool__(self) -> bool: # type: ignore
		return 1 in self._bits

	def __hash__(self) -> int: # type: ignore
		return hash(tuple(self._bits))

	def __format__(self, format_spec: str) -> str: # type: ignore
		return f'_MultipleBits({self._bits:{format_spec}})' 

	# def __dir__(self) -> Iterable[str]: # type: ignore
		# pass

	def __getitem__(self, index: int) -> Bit:
		if index < 0:
			# negative index, translate to absolute first
			index = self._len + index
		if index < 0 or index > self._len-1:
			raise IndexError("Index out of range "+str(self._len))
		return self._bits[index]
	
	def __setitem__(self, index: int, value: Bit) -> None:
		if not isinstance(value, Bit):
			raise ValueError("_MultipleBits can only contain bits")
		
		if index < 0:
			# negative index, translate to absolute first
			index = self._len + index
		if index < 0 or index > self._len-1:
			raise IndexError("Index out of range "+str(self._len))
		
		self._bits[index] = value

	def __iter__(self):
		for bit in self._bits:
			yield bit

	# BINARY OPERATORS
	def __add__(self, other: Any) -> _MultipleBits: # type: ignore
		return _MultipleBits(self._bits + other)

	def __sub__(self, other: Any) -> _MultipleBits: # type: ignore
		return _MultipleBits(self._bits - other)
		
	def __mul__(self, other: Any) -> _MultipleBits: # type: ignore
		return _MultipleBits(self._bits * other)

	def __truediv__(self, other: Any) -> _MultipleBits: # type: ignore
		raise NotImplementedError

	def __floordiv__(self, other: Any) -> _MultipleBits: # type: ignore
		raise NotImplementedError

	def __mod__(self, other: Any) -> _MultipleBits: # type: ignore
		raise NotImplementedError

	def __pow__(self, other: Any) -> _MultipleBits: # type: ignore
		raise NotImplementedError

	# ASSIGNMENT OPERATORS
	def __iadd__(self, other: Any) -> _MultipleBits: # type: ignore
		self = self.__add__(other)

	def __isub__(self, other: Any) -> _MultipleBits: # type: ignore
		self = self.__sub__(other)

	def __imul__(self, other: Any) -> _MultipleBits: # type: ignore
		self = self.__mul__(other)

	def __idiv__(self, other: Any) -> _MultipleBits: # type: ignore
		self = self.__div__(other)

	def __ifloordiv__(self, other: Any) -> _MultipleBits: # type: ignore
		self = self.__floordiv__(other)

	def __imod__(self, other: Any) -> _MultipleBits: # type: ignore
		self = self.__mod__(other)

	def __ipow__(self, other: Any) -> _MultipleBits: # type: ignore
		self = self.__pow__(other)

	# COMPARISON OPERATORS
	def __lt__(self, other: Any) -> bool: # type: ignore
		return self.to_int() < other.to_int() if isinstance(other, _MultipleBits) else self.to_int() < other

	def __gt__(self, other: Any) -> bool: # type: ignore
		return self.to_int() > other.to_int() if isinstance(other, _MultipleBits) else self.to_int() > other

	def __le__(self, other: Any) -> bool: # type: ignore
		return self.to_int() <= other.to_int() if isinstance(other, _MultipleBits) else self.to_int() <= other

	def __ge__(self, other: Any) -> bool: # type: ignore
		return self.to_int() >= other.to_int() if isinstance(other, _MultipleBits) else self.to_int() >= other

	def __eq__(self, other: Any) -> bool: # type: ignore
		return self._bits == other._bits if isinstance(other, _MultipleBits) else self.to_int() == other

	def __ne__(self, other: Any) -> bool: # type: ignore
		return self._bits != other._bits if isinstance(other, _MultipleBits) else self.to_int() != other

	# UNARY OPERATORS
	def __neg__(self) -> _MultipleBits: # type: ignore
		return [-bit for bit in self._bits]

	def __pos__(self) -> _MultipleBits: # type: ignore
		return [-abs(bit) for bit in self._bits]

	def __invert__(self) -> _MultipleBits: # type: ignore
		not self._bits
	
	# METHODS
	def to_list(self) -> List[int]:
		"""return bits as a list of zeros and ones"""
		return [1 if bit else 0 for bit in self._bits]

	def to_int(self) -> int:
		"""return bits as a decimal integer"""
		return _bits_to_int(self.to_list())

	def to_hex(self) -> str:
		"""return bits as a hexadecimal string"""
		return _bits_to_hex(self.to_list())

class Byte(_MultipleBits):
	"""Represents a single byte"""

	def __init__(self, *args: Union[List[Bit], Bit, int, str]) -> Byte:
		err = "Bytes can take a list, 8 objects, an int between 0 and 256, a string with 8 zeros or ones or a single character"
		bits: List[Bit] = []

		if len(args) == 1:
			arg = args[0]
			
			if isinstance(arg, list):
				# # must be list of Bit instances
				# if not all(isinstance(x, Bit) for x in arg):
				# 	raise ValueError(err)
				bits = [Bit(x) for x in arg]

			elif isinstance(arg, str):
				# must be str with one char
				if len(arg) == 1:
					# char
					intarg = ord(arg)
					if intarg < 0 or intarg > 255:
						raise ValueError(err)
					bits = _int_to_bits(intarg, length=8)
				
				elif len(arg) == 8 and all(c in '01' for c in arg):
					# string like '00001111'
					bits = [int(x) for x in arg]
				
				else:
					raise ValueError(err)

			elif isinstance(arg, int):
				# must be unsigned uint8 kinda int
				if arg < 0 or arg > 255:
					raise ValueError(err)
				bits = _int_to_bits(arg, length=8)

			bits = [Bit(x) for x in bits]

		elif len(args) == 8:
			# expect 8x any object
			for arg in args:
				bits.append(Bit(arg))

		else:
			raise ValueError(err)

		super().__init__(bits)

	def __repr__(self) -> str:
		return f"Byte({self.to_int()})"

class Nibble(_MultipleBits):
	"""Represents a single nibble"""

	def __init__(self, *args: Union[List[Bit], Bit, int, str]) -> Byte:
		err = "Nibbles can take a list, 4 objects, an int between 0 and 16, a string with 4 zeros or ones or a single character"
		bits: List[Bit] = []

		if len(args) == 1:
			arg = args[0]
			
			if isinstance(arg, list):
				# # must be list of Bit instances
				# if not all(isinstance(x, Bit) for x in arg):
				# 	raise ValueError(err)
				[Bit(x) for x in arg]
				bits = arg

			elif isinstance(arg, str):
				# must be str with one char
				if len(arg) == 1:
					# char
					intarg = ord(arg)
					if intarg < 0 or intarg > 15:
						raise ValueError(err)
					bits = _int_to_bits(intarg, length=4)
				
				elif len(arg) == 4 and all(c in '01' for c in arg):
					# string like '00001111'
					bits = [int(x) for x in arg]
				
				else:
					raise ValueError(err)

			elif isinstance(arg, int):
				# must be unsigned uint8 kinda int
				if arg < 0 or arg > 15:
					raise ValueError(err)
				bits = _int_to_bits(arg, length=4)

			bits = [Bit(x) for x in bits]

		elif len(args) == 4:
			# expect 8x any object
			for arg in args:
				bits.append(Bit(arg))

		else:
			raise ValueError(err)

		super().__init__(bits)

	def __repr__(self) -> str:
		return f"Nibble({self.to_int()})"

class ByteLike(_MultipleBits):
	"""Represents an immutable amount of bits"""

	def __init__(self, *args: Union[List[Bit], Bit, int, str], size: int = False) -> Byte:
		err = "ByteLikes can take a list, X objects, an int, a string with zeros or ones or a single character"
		bits: List[Bit] = []

		if len(args) == 1:
			arg = args[0]

			if isinstance(arg, list):
				## must be list of Bit instances
				# if not all(isinstance(x, Bit) for x in arg):
					# raise ValueError(err)
				bits = [Bit(x) for x in arg]

			elif isinstance(arg, str):
				# must be str with one char
				if len(arg) == 1:
					# char
					intarg = ord(arg)
					if size and intarg < 0 or intarg > _bits_to_int([1]*size):
						raise ValueError(err)
					bits = _int_to_bits(intarg, length=size)

				elif all(c in '01' for c in arg):
					if size and len(arg) != size:
						raise ValueError 
					# string like '00001111'
					bits = [int(x) for x in arg]

				else:
					raise ValueError(err)

			elif isinstance(arg, int):
				# must be unsigned uint8 kinda int
				if size and (arg < 0 or arg > _bits_to_int([1]*size)):
					raise ValueError(err)
				bits = _int_to_bits(arg, length=size)

			bits = [Bit(x) for x in bits]

		elif not size or len(args) == size:
			# expect 8x any object
			for arg in args:
				bits.append(Bit(arg))

		else:
			raise ValueError(err)

		super().__init__(bits)

	def __repr__(self) -> str:
		return f"ByteLike({self._bits})"









