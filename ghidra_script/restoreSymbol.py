#TODO write a description for this script
#@author 
#@category _NEW_
#@keybinding 
#@menupath 
#@toolbar 
#@runtime Jython


#TODO Add User Code Here

START = getMemoryBlock(".gopclntab")
TEXT_START = getMemoryBlock(".text")

if not START or not TEXT_START: 
    # It's possible that the .gopclntab and .text memory blocks are not found in the current program,
    # due to hard stripping for example.

    #But you can still find them by parsing all the memory blocks 
    #searching for magics
    # START = findMagicsPcnltab()...
    exit()

START = START.getStart()
TEXT_START = TEXT_START.getStart()

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
    pc = TEXT_START.add(pc_offset)

    # Function Name 
    funcdata_offset = getInt(func_data_addr.add(4))
    funcdata_addr = FUNCTAB.add(funcdata_offset)
    funcname_offset = getInt(funcdata_addr.add(4))
    string_name_addr = FUNCNAMETAB.add(funcname_offset)

    func_string = ""
    curr_addr = string_name_addr
    
    c = '' 
    #just a reminder: from here you have to fetch each byte until you reach a 0
    while c != '\x00':
        b = getByte(curr_addr)        
        c = chr(b & 0xFF)        
        if c != '\x00':
            func_string += c            
        curr_addr = curr_addr.add(1)

    #clean functions with special characters due to errors in Ghidra
    func_name = func_string
    special_chr = [' ', '*', '(', ')', '[', ']', '{', '}', ',', '<', '>',' ']
    for char in special_chr:
        func_name = func_name.replace(char, '_')

    # Association 
    if func_name:
        createLabel(pc, func_name, True)

    i += 1
    
    



