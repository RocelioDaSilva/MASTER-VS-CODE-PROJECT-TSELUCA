$port = 8000
$url = "http://localhost:$port/"
$listener = New-Object System.Net.HttpListener
$listener.Prefixes.Add($url)
$listener.Start()

Write-Host "Server running at http://localhost:8000"
Write-Host "Press Ctrl+C to stop the server"

$docRoot = "c:\Users\PCGAME\Desktop\website building"

# MIME type mapping
$mimeTypes = @{
    ".html" = "text/html; charset=utf-8"
    ".css"  = "text/css; charset=utf-8"
    ".js"   = "application/javascript; charset=utf-8"
    ".json" = "application/json; charset=utf-8"
    ".xml"  = "application/xml; charset=utf-8"
    ".txt"  = "text/plain; charset=utf-8"
    ".png"  = "image/png"
    ".jpg"  = "image/jpeg"
    ".jpeg" = "image/jpeg"
    ".gif"  = "image/gif"
    ".svg"  = "image/svg+xml"
    ".ico"  = "image/x-icon"
    ".webp" = "image/webp"
    ".woff" = "font/woff"
    ".woff2"= "font/woff2"
    ".ttf"  = "font/ttf"
    ".pdf"  = "application/pdf"
}

while ($listener.IsListening) {
    $context = $listener.GetContext()
    $request = $context.Request
    $response = $context.Response
    
    $requestPath = $request.Url.LocalPath
    if ($requestPath -eq "/") {
        $requestPath = "/index.html"
    }
    
    $filePath = Join-Path $docRoot ($requestPath -replace "^/", "")
    
    if (Test-Path $filePath) {
        $fileContent = [System.IO.File]::ReadAllBytes($filePath)
        $extension = [System.IO.Path]::GetExtension($filePath).ToLower()
        $contentType = if ($mimeTypes.ContainsKey($extension)) { $mimeTypes[$extension] } else { "application/octet-stream" }
        $response.ContentType = $contentType
        $response.ContentLength64 = $fileContent.Length
        $response.OutputStream.Write($fileContent, 0, $fileContent.Length)
    } else {
        # Serve 404.html if it exists
        $notFoundPath = Join-Path $docRoot "404.html"
        if (Test-Path $notFoundPath) {
            $response.StatusCode = 404
            $response.ContentType = "text/html; charset=utf-8"
            $fileContent = [System.IO.File]::ReadAllBytes($notFoundPath)
            $response.ContentLength64 = $fileContent.Length
            $response.OutputStream.Write($fileContent, 0, $fileContent.Length)
        } else {
            $response.StatusCode = 404
            $response.ContentType = "text/plain"
            $message = "404 - File not found"
            $buffer = [System.Text.Encoding]::UTF8.GetBytes($message)
            $response.OutputStream.Write($buffer, 0, $buffer.Length)
        }
    }
    
    $response.OutputStream.Close()
}

$listener.Stop()
