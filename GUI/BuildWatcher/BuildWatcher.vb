Imports System.Text

Public Class BuildWatcher

    Private Sub LaunchAnalyzer(amount As String, fileName As String)
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

        Dim command As String = "python C:\Projects\BuildWatcher\BuildConsole Scraper\TCScraper.py " & amount & " """ & fileName & """ >> C:\Projects\BuildWatcher\BuildConsole Scraper\logs.txt"

        SW.WriteLine(command)
        SW.WriteLine("exit")

        SW.Close()
        SR.Close()
    End Sub

    Private Sub ReadCSV()
        Dim fileName As String = InputBox("Name of the field containing the data:", "Open file", "errors")
        Dim filePath As String = "C:\Projects\BuildWatcher\BuildConsole Scraper\" & fileName & ".csv"
        Dim TextLine As String = ""
        Dim SplitLine() As String

        If System.IO.File.Exists(filePath) = True Then
            Using objReader As New System.IO.StreamReader(filePath, Encoding.ASCII)
                Me.DataGridView1.Rows.Clear()
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
        Dim fileName As String = InputBox("Name for the results file:", "Launch", "errors")
        amount = TextBox1.Text
        LaunchAnalyzer(amount, fileName)
    End Sub

    Private Sub Button3_Click(sender As Object, e As EventArgs) Handles Button3.Click
        Dim logsPath As String = "C:\Projects\BuildWatcher\BuildConsole Scraper\logs.txt"
        If System.IO.File.Exists(logsPath) = True Then
            Me.DataGridView1.Hide()
            Me.TextBox2.Show()
            TextBox2.Text = System.IO.File.ReadAllText(logsPath)
            'Process.Start(logsPath)
        Else
            MsgBox("File Does Not Exist")
        End If
    End Sub

    Private Sub Button4_Click(sender As Object, e As EventArgs) Handles Button4.Click
        Me.DataGridView1.Show()
        Me.TextBox2.Hide()
    End Sub
End Class
