from PyPlcnextRsc.common.internalEnums.string_encoding import RscStringEncoding
from PyPlcnextRsc.common.objects import *
from PyPlcnextRsc.common.serviceDefinition.marshal import *
from PyPlcnextRsc.common.serviceDefinition.proxy import *
from PyPlcnextRsc.common.tag_type import *
from PyPlcnextRsc.common.types import *

# DO NOT REMOVE NEXT LINES:
# FOR PREVENT IDE AUTO CLEAN IMPORT
RemotingMethod
RscVariant

# -----------------------

RscString512 = RscTpAnnotate[str, Marshal(rscStringEncoding=RscStringEncoding.Utf8, maxStringSize=512)]
RscString64 = RscTpAnnotate[str, Marshal(rscStringEncoding=RscStringEncoding.Utf8, maxStringSize=64)]
RscString128 = RscTpAnnotate[str, Marshal(rscStringEncoding=RscStringEncoding.Utf8, maxStringSize=128)]
RscSecureString128 = RscTpAnnotate[str, Marshal(rscType=RscType.SecureString, rscStringEncoding=RscStringEncoding.Utf8, maxStringSize=128)]

# Uint8 = RscTpAnnotate[int, Marshal(rscType=RscType.Uint8)]
# Uint16 = RscTpAnnotate[int, Marshal(rscType=RscType.Uint16)]
# Uint32 = RscTpAnnotate[int, Marshal(rscType=RscType.Uint32)]
# Uint64 = RscTpAnnotate[int, Marshal(rscType=RscType.Uint64)]
# Int8 = RscTpAnnotate[int, Marshal(rscType=RscType.Int8)]
# Int16 = RscTpAnnotate[int, Marshal(rscType=RscType.Int16)]
# Int32 = RscTpAnnotate[int, Marshal(rscType=RscType.Int32)]
# Int64 = RscTpAnnotate[int, Marshal(rscType=RscType.Int64)]

Uint8 = RscTpAnnotate[int, RscType.Uint8]
Uint16 = RscTpAnnotate[int, RscType.Uint16]
Uint32 = RscTpAnnotate[int, RscType.Uint32]
Uint64 = RscTpAnnotate[int, RscType.Uint64]
Int8 = RscTpAnnotate[int, RscType.Int8]
Int16 = RscTpAnnotate[int, RscType.Int16]
Int32 = RscTpAnnotate[int, RscType.Int32]
Int64 = RscTpAnnotate[int, RscType.Int64]
