#!/usr/bin/env python3
import http.server
import socketserver
import subprocess
import threading
import webbrowser
import time
import os
import json

PORT = 8000

html = """
<!DOCTYPE html>
<html>
<head>
<title>Deployment Terminal</title>
<style>
  body { background: #0a0a0a; color: #00ff00; font-family: 'Courier New', Courier, monospace; padding: 30px; margin: 0; }
  h2 { color: #ffffff; text-shadow: 0 0 5px #00ff00; margin-bottom: 5px; }
  #terminal { 
      height: 60vh; 
      overflow-y: auto; 
      border: 1px solid #333; 
      padding: 15px; 
      background: #000;
      white-space: pre-wrap;
      word-wrap: break-word;
      border-radius: 4px;
      box-shadow: inset 0 0 10px #000;
      font-size: 14px;
  }
  .progress-container { width: 100%; background-color: #222; margin-top: 15px; border-radius: 4px; border: 1px solid #444; }
  .progress-bar { width: 0%; height: 25px; background-color: #00ff00; text-align: center; line-height: 25px; color: #000; font-weight: bold; font-family: sans-serif; transition: width 0.1s;}
  .stage-indicator { margin-top: 5px; margin-bottom: 15px; font-size: 1.2em; color: #ffeb3b; font-weight: bold; }
  
  /* Scrollbar */
  ::-webkit-scrollbar { width: 8px; }
  ::-webkit-scrollbar-track { background: #111; }
  ::-webkit-scrollbar-thumb { background: #444; border-radius: 4px; }
  ::-webkit-scrollbar-thumb:hover { background: #555; }
</style>
</head>
<body>
  <h2>🚀 Auto-Deploy Terminal</h2>
  <div id="stage" class="stage-indicator">Waiting for stream...</div>
  <div class="progress-container">
    <div id="progress-bar" class="progress-bar">0%</div>
  </div>
  <br>
  <div id="terminal"></div>
  
  <script>
    var source = new EventSource("/stream");
    var terminal = document.getElementById("terminal");
    var progressBar = document.getElementById("progress-bar");
    var stage = document.getElementById("stage");
    
    var autoScroll = true;
    terminal.addEventListener('scroll', function() {
        autoScroll = (terminal.scrollTop + terminal.clientHeight >= terminal.scrollHeight - 10);
    });

    source.onmessage = function(event) {
        var data = JSON.parse(event.data);
        if (data.type === 'log') {
            var div = document.createElement('div');
            div.textContent = "> " + data.text;
            terminal.appendChild(div);
            while(terminal.childNodes.length > 500) {
                terminal.removeChild(terminal.firstChild);
            }
            if (autoScroll) {
                terminal.scrollTop = terminal.scrollHeight;
            }
        } else if (data.type === 'progress') {
            progressBar.style.width = data.percent + "%";
            progressBar.innerHTML = data.percent + "%";
        } else if (data.type === 'stage') {
            stage.innerHTML = data.text;
        } else if (data.type === 'done') {
            source.close();
            stage.innerHTML = "✅ Deployment Complete!";
            stage.style.color = "#00ff00";
        }
    };
    source.onerror = function() {
        source.close();
    };
  </script>
</body>
</html>
"""

class DeploymentServer(http.server.SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        pass # Suppress standard HTTP logs

    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(html.encode('utf-8'))
        elif self.path == '/stream':
            self.send_response(200)
            self.send_header('Content-type', 'text/event-stream')
            self.send_header('Cache-Control', 'no-cache')
            self.send_header('Connection', 'keep-alive')
            self.end_headers()
            
            def send_msg(msg_type, content):
                data = json.dumps({'type': msg_type, 'text': content.strip() if msg_type != 'progress' else None, 'percent': content if msg_type == 'progress' else None})
                try:
                    self.wfile.write(f"data: {data}\n\n".encode('utf-8'))
                    self.wfile.flush()
                except:
                    pass

            try:
                # Stage 0: Count
                send_msg('stage', 'Counting files...')
                send_msg('log', 'Finding total files in public_html_local...')
                proc = subprocess.Popen(['find', 'public_html_local', '-type', 'f'], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
                out, _ = proc.communicate()
                total_files = max(1, out.count(b'\n'))
                send_msg('log', f'Found {total_files} files ready for transfer.')
                
                # Stage 1: Compress
                send_msg('stage', '📦 Stage 1/3: Compressing site files...')
                send_msg('progress', 0)
                
                cmd_tar = ['tar', '-czvf', 'site_payload.tar.gz', '-C', 'public_html_local', '.']
                proc_tar = subprocess.Popen(cmd_tar, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1)
                
                files_processed = 0
                last_update_time = time.time()
                for line in proc_tar.stdout:
                    files_processed += 1
                    if time.time() - last_update_time > 0.05: # Send at most 20 FPS to browser
                        percent = min(100, int((files_processed / total_files) * 100))
                        send_msg('progress', percent)
                        send_msg('log', line)
                        last_update_time = time.time()
                proc_tar.wait()
                send_msg('progress', 100)
                send_msg('log', 'Archive created successfully.')
                
                # Stage 2: Upload
                send_msg('stage', '🚀 Stage 2/3: Uploading payload archive to Hostinger...')
                send_msg('progress', 0)
                ssh_key = os.path.expanduser('~/.ssh/id_ed25519')
                cmd_rsync = ['rsync', '-a', '-e', f'ssh -p 65002 -i {ssh_key} -o StrictHostKeyChecking=no', '--info=progress2', 'site_payload.tar.gz', 'u803913036@82.198.228.154:domains/skyautoservices.com/public_html/']
                proc_rsync = subprocess.Popen(cmd_rsync, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=1, universal_newlines=True)
                
                buf = ""
                while True:
                    c = proc_rsync.stdout.read(1)
                    if not c:
                        break
                    if c == '\r' or c == '\n':
                        if buf:
                            if '%' in buf:
                                try:
                                    parts = buf.split('%')[0].split()
                                    percent = int(parts[-1])
                                    send_msg('progress', percent)
                                except:
                                    pass
                            send_msg('log', buf)
                            buf = ""
                    else:
                        buf += c
                proc_rsync.wait()
                send_msg('progress', 100)
                send_msg('log', 'Upload complete.')
                
                # Stage 3: Extract
                send_msg('stage', '🔓 Stage 3/3: Extracting files on server...')
                send_msg('progress', 100)
                send_msg('log', 'Executing remote extraction via SSH...')
                cmd_ssh = f'ssh -p 65002 -i {ssh_key} -o StrictHostKeyChecking=no u803913036@82.198.228.154 "cd domains/skyautoservices.com/public_html && tar -xzf site_payload.tar.gz && rm site_payload.tar.gz"'
                proc_ssh = subprocess.Popen(cmd_ssh, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, shell=True)
                for line in proc_ssh.stdout:
                    send_msg('log', line)
                proc_ssh.wait()
                send_msg('log', 'Extraction complete.')
                
                # Stage 4: Cleanup
                send_msg('stage', '🧹 Stage 4: Cleaning up...')
                if os.path.exists('site_payload.tar.gz'):
                  self.wfile.write(f"data: {json.dumps({'type': 'step', 'message': 'Cleaning up local archive...'})}\n\n".encode('utf-8'))
                subprocess.run(['rm', '-f', 'site_payload.tar.gz'], check=True)

                # NEW CACHE CLEARING STEP
                self.wfile.write(f"data: {json.dumps({'type': 'step', 'message': 'Clearing Hostinger cache...'})}\n\n".encode('utf-8'))
                # Touch litespeed purge file and send HTTP PURGE request
                purge_cmd = [
                    'ssh', '-p', '65002', '-i', os.path.expanduser('~/.ssh/id_ed25519'), '-o', 'StrictHostKeyChecking=no',
                    'u803913036@82.198.228.154',
                    'cd domains/skyautoservices.com/public_html && touch .litespeed_purge && rm -f .litespeed_purge'
                ]
                subprocess.run(purge_cmd, capture_output=True)
                subprocess.run(['curl', '-s', '-X', 'PURGE', 'https://skyautoservices.com/'], capture_output=True)

                self.wfile.write(f"data: {json.dumps({'type': 'step', 'message': 'All site files successfully deployed and cache cleared!'})}\n\n".encode('utf-8'))
                send_msg('done', '')

            except Exception as e:
                send_msg('log', f"ERROR: {str(e)}")
            
            # Close the server after completion
            def shutdown():
                time.sleep(2)
                os._exit(0)
            threading.Thread(target=shutdown).start()

def run_server():
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), DeploymentServer) as httpd:
        print(f"Starting auto-deploy UI...")
        print(f"Opening browser at http://localhost:{PORT}")
        try:
            webbrowser.open(f"http://localhost:{PORT}")
        except:
            pass
        httpd.serve_forever()

if __name__ == '__main__':
    run_server()
