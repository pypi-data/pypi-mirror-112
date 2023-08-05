class TofuDetection(Exception): pass # Exception for Tofu.
class AsciiDetection(Exception): pass # Exception for Ascii.
def CharacterMap():
    """Character map."""
    import os
    os.system('charmap.exe')
def TofuDetector(var=''):
    """Detects if a tofu (character backslash-x1b) is in var."""
    if '\x1b' in var:
        raise TofuDetection('Tofu detected in the variable.')
    else:
        raise TofuDetection('No tofu detected in the variable.')
def AsciiDetector(var=''):
    """Detects if var is ASCII."""
    if var.isascii():
        raise AsciiDetection('The variable is ASCII.')
    else:
        raise AsciiDetection('The variable is not ASCII.')
