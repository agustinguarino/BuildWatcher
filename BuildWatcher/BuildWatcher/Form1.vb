Imports System.Text

Public Class Form1

    Private Sub LaunchAnalyzer(amount As String)
        Dim myprocess As New Process
        Dim StartInfo As New System.Diagnostics.ProcessStartInfo

        StartInfo.FileName = "cmd"
        StartInfo.RedirectStandardInput = True
        StartInfo.RedirectStandardOutput = True
        StartInfo.CreateNoWindow = True
        StartInfo.UseShellExecute = False
        myprocess.StartInfo = StartInfo
        myprocess.Start()

        Dim SR As System.IO.StreamReader = myprocess.StandardOutput
        Dim SW As System.IO.StreamWriter = myprocess.StandardInput

        Dim command As String
        command = "python C:\Projects\BuildWatcher\TCScraper.py " & amount & " > C:\Projects\BuildWatcher\logs.txt"
        MsgBox(command)

        SW.WriteLine(command)
        SW.WriteLine("exit")

        SW.Close()
        SR.Close()
    End Sub

    Private Sub ReadCSV()
        Dim fName As String = "C:\Projects\BuildWatcher\errors.csv"
        Dim TextLine As String = ""
        Dim SplitLine() As String

        If System.IO.File.Exists(fName) = True Then
            Using objReader As New System.IO.StreamReader(fName, Encoding.ASCII)
                Do While objReader.Peek() <> -1
                    TextLine = objReader.ReadLine()
                    SplitLine = Split(TextLine, ",")
                    Me.DataGridView1.Rows.Add(SplitLine)
                    Me.DataGridView1.Rows(0).Visible = False
                Loop
            End Using
        Else
            MsgBox("File Does Not Exist")
            Me.DataGridView1.Rows.Clear()
        End If
    End Sub

    Private Sub Button2_Click(sender As Object, e As EventArgs) Handles Button2.Click
        ReadCSV()
    End Sub

    Private Sub Button1_Click(sender As Object, e As EventArgs) Handles Button1.Click
        Dim amount As String
        amount = TextBox1.Text
        LaunchAnalyzer(amount)
    End Sub

    Private Sub Button3_Click(sender As Object, e As EventArgs) Handles Button3.Click
        Dim logsPath As String = "C:\Projects\BuildWatcher\logs.txt"
        If System.IO.File.Exists(logsPath) = True Then
            Process.Start(logsPath)
        Else
            MsgBox("File Does Not Exist")
        End If
    End Sub
End Class
