' Export SZmax(2),Zmin(1) from the currently opened CST project.
' 导出当前 CST 工程中的 SZmax(2),Zmin(1) 结果。

Sub Main()
    Dim treePath As String
    Dim outputPath As String
    Dim resultId As String
    Dim r As Object
    Dim i As Long
    Dim reVal As Double
    Dim imVal As Double
    Dim magVal As Double
    Dim fn As Integer

    treePath = "1D Results\S-Parameters\SZmax(2),Zmin(1)"
    outputPath = "E:\aris\meta\cst_coupling_model1\data\raw\periodic\model1_szmax2_zmin1_export_test.csv"
    resultId = GetLastResultID()

    Set r = Resulttree.GetResultFromTreeItem(treePath, resultId)

    fn = FreeFile
    Open outputPath For Output As #fn
    Print #fn, "frequency_ghz,real,imag,magnitude"

    For i = 0 To r.GetN() - 1
        reVal = r.GetYRe(i)
        imVal = r.GetYIm(i)
        magVal = Sqr(reVal * reVal + imVal * imVal)
        Print #fn, CStr(r.GetX(i)) & "," & CStr(reVal) & "," & CStr(imVal) & "," & CStr(magVal)
    Next i

    Close #fn
End Sub
