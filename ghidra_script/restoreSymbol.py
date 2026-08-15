#TODO write a description for this script
#@author 
#@category _NEW_
#@keybinding 
#@menupath 
#@toolbar 
#@runtime Jython


#TODO Add User Code Here

START = getMemoryBlock(".gopclntab").getStart()
TEXT_START = getMemoryBlock(".text").getStart()

if not START or not TEXT_START: 
    # It's possible that the .gopclntab and .text memory blocks are not found in the current program,
    # due to hard stripping.

    #But you can still find them by parsing all the momeory blocks 
    #searching for magics
    # START = findMagicsPcnltab()...
    exit()

PTRSIZE = currentProgram.getDefaultPointerSize()

FUNCNAMETAB_OFFSET = getInt(START.add(0x08 + (3 * PTRSIZE)))
FUNCNAMETAB = START.add(FUNCNAMETAB_OFFSET)

FUNCTAB_OFFSET = getInt(START.add(0x08 + (7 * PTRSIZE)))
FUNCTAB = START.add(FUNCTAB_OFFSET)

NFUNCTAB = getInt(START.add(0x08))

i = 0 

while i < NFUNCTAB: 
    func_data_addr = FUNCTAB.add(i * 8)

    # PC
    pc_offset = getInt(func_data_addr)
    pc = getInt(TEXT_START.add(pc_offset))

    # Function Name 
    funcdata_offset = getInt(func_data_addr.add(4))
    funcdata_addr = FUNCTAB.add(funcdata_offset)
    funcname_offset = getInt(funcdata_addr.add(4))
    string_name_addr = FUNCNAMETAB.add(funcname_offset)

    string_name = ""
    chr = ''
    while chr != '\x00':
        chr = getByte(string_name_addr)
        string_name += chr
        string_name_addr = string_name_addr.add(1)

    # Association 
    createLabel(string_name_addr, string_name, True)

    i += 1
    
    



