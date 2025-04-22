Option Explicit

Dim fso, origem, destino, shell
Dim mensagemSucesso, mensagemErro, titulo

Set fso = CreateObject("Scripting.FileSystemObject")
Set shell = CreateObject("WScript.Shell")

origem = "C:\sis_orc\Sis_Orc.lnk"
destino = shell.SpecialFolders("Desktop") & "\Sis_Orc.lnk"

mensagemSucesso = "Atalho copiado para a Area de trabalho com sucesso!"
mensagemErro = "O arquivo """ & origem & """ nao foi encontrado."
titulo = "Informacao"

If fso.FileExists(origem) Then
    On Error Resume Next
    fso.CopyFile origem, destino, True
    If Err.Number = 0 Then
        MsgBox mensagemSucesso, vbInformation, titulo
    Else
        MsgBox "Erro ao copiar o atalho!", vbCritical, titulo
    End If
    On Error GoTo 0
Else
    MsgBox mensagemErro, vbCritical, titulo
End If
