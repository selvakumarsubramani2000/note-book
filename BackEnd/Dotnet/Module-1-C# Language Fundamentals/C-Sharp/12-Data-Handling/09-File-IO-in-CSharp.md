# 📁 File I/O in C#

> **Trainer's Note:** File I/O means reading and writing files. Start with simple helpers in `System.IO`, then learn streams when you need more control.

---

## 📑 Table of Contents
1. [What is File I/O?](#1-what-is-file-io)
2. [File and FileInfo Basics](#2-file-and-fileinfo-basics)
3. [Read and Write Text](#3-read-and-write-text)
4. [Directories and Common Patterns](#4-directories-and-common-patterns)
5. [Knowledge Check](#5-knowledge-check)

---

## 1. What is File I/O?

**I/O = Input/Output**
- Input → read data from file
- Output → write data to file

Namespace: `System.IO`

### Real-world analogy
```
File        = notebook
File.Read   = open notebook and read page
File.Write  = write new notes on page
Directory   = cupboard holding notebooks
```

---

## 2. File and FileInfo Basics

### Static helper: `File`
```csharp
using System.IO;

string path = @"C:\Temp\notes.txt";

if (!File.Exists(path))
    File.WriteAllText(path, "Hello File");

string content = File.ReadAllText(path);
File.AppendAllText(path, "\nSecond line");
File.Copy(path, @"C:\Temp\notes-copy.txt", overwrite: true);
// File.Delete(path);
```

### Instance helper: `FileInfo`
```csharp
FileInfo fi = new FileInfo(path);
Console.WriteLine(fi.Exists);
Console.WriteLine(fi.Length);
Console.WriteLine(fi.Extension);
Console.WriteLine(fi.FullName);
```

Use `File` for quick one-line operations. Use `FileInfo` when working repeatedly with the same file metadata.

---

## 3. Read and Write Text

### Write / read all lines
```csharp
string[] lines =
{
    "Line 1",
    "Line 2",
    "Line 3"
};

File.WriteAllLines(@"C:\Temp\lines.txt", lines);
string[] readBack = File.ReadAllLines(@"C:\Temp\lines.txt");
```

### StreamWriter / StreamReader (more control)
```csharp
using (StreamWriter writer = new StreamWriter(@"C:\Temp\log.txt", append: true))
{
    writer.WriteLine($"{DateTime.Now}: app started");
}

using (StreamReader reader = new StreamReader(@"C:\Temp\log.txt"))
{
    string? line;
    while ((line = reader.ReadLine()) != null)
        Console.WriteLine(line);
}
```

`using` ensures file handles are closed even if errors happen.

### Async style (modern apps)
```csharp
await File.WriteAllTextAsync(path, "async write");
string text = await File.ReadAllTextAsync(path);
```

---

## 4. Directories and Common Patterns

### Directory operations
```csharp
string dir = @"C:\Temp\Reports";
Directory.CreateDirectory(dir);

string[] files = Directory.GetFiles(dir, "*.txt");
foreach (string file in files)
    Console.WriteLine(file);

// Directory.Delete(dir, recursive: true);
```

### Path helpers (very useful)
```csharp
string folder = @"C:\Temp";
string full = Path.Combine(folder, "data", "file.txt");
string ext = Path.GetExtension(full);
string name = Path.GetFileName(full);
string nameNoExt = Path.GetFileNameWithoutExtension(full);
```

Always prefer `Path.Combine` over manual string concatenation.

### Practical safe pattern
```csharp
try
{
    string path = Path.Combine(@"C:\Temp", "orders.csv");
    File.WriteAllText(path, "Id,Amount\n1,500");
}
catch (DirectoryNotFoundException)
{
    Console.WriteLine("Folder not found");
}
catch (IOException ex)
{
    Console.WriteLine($"I/O failed: {ex.Message}");
}
catch (UnauthorizedAccessException)
{
    Console.WriteLine("Permission denied");
}
```

### Beginner tips
| Tip | Why |
|-----|-----|
| Check `Exists` before delete/read assumptions | Avoid avoidable crashes |
| Use `using` for readers/writers | Close files properly |
| Prefer async APIs in web apps | Better scalability |
| Handle I/O exceptions | Disk/permission issues are common |
| Don't hardcode paths everywhere | Use config + `Path.Combine` |

---

## 5. Knowledge Check

1. Which namespace is used for File I/O?
2. Difference between `File` and `FileInfo`?
3. Why is `using` important with `StreamReader`/`StreamWriter`?
4. What does `Path.Combine` help with?
5. Name 3 exceptions you might catch during file operations.

---

**Previous:** [← Custom Exceptions](./08-Custom-Exceptions.md)

🎉 **Done!** You completed the Data Handling track: nullables, struct/class, enums, operators, namespaces, directives, regex, exceptions, and file I/O.
