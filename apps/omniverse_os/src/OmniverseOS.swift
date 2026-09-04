//
//  OmniverseOS.swift
//  Omniverse OS - Native macOS Standalone Application
//  Apex Workstation Substrate Virtual Machine
//  Architecture: Zen 5 96C/192T | WRX90 | DDR5-6400 | PCIe 5.0 RAID 0 | RTX 5090
//

import Cocoa
import WebKit

class MainWindowController: NSWindowController, NSWindowDelegate {
    var webView: WKWebView!
    var process: Process?

    convenience init() {
        let screenRect = NSScreen.main?.visibleFrame ?? NSRect(x: 0, y: 0, width: 1440, height: 900)
        let width = min(1360.0, screenRect.width - 40.0)
        let height = min(860.0, screenRect.height - 40.0)

        let window = NSWindow(
            contentRect: NSRect(x: 0, y: 0, width: width, height: height),
            styleMask: [.titled, .closable, .miniaturizable, .resizable, .fullSizeContentView],
            backing: .buffered,
            defer: false
        )
        self.init(window: window)
        
        window.title = "Omniverse OS (Build 2026.9995 - Apex Workstation Virtual Machine)"
        window.titleVisibility = .hidden
        window.titlebarAppearsTransparent = true
        window.isMovableByWindowBackground = true
        window.appearance = NSAppearance(named: .darkAqua)
        window.backgroundColor = NSColor(calibratedRed: 7/255, green: 10/255, blue: 18/255, alpha: 1.0)
        window.center()
        window.delegate = self

        // WKWebView Configuration
        let config = WKWebViewConfiguration()
        config.preferences.setValue(true, forKey: "developerExtrasEnabled")
        
        webView = WKWebView(frame: window.contentView!.bounds, configuration: config)
        webView.autoresizingMask = [.width, .height]
        webView.setValue(false, forKey: "drawsBackground")
        window.contentView?.addSubview(webView)

        // Ensure background kernel daemon is active
        startKernelDaemon()

        // Load Omniverse OS Desktop Interface
        DispatchQueue.main.asyncAfter(deadline: .now() + 0.4) { [weak self] in
            if let url = URL(string: "http://127.0.0.1:8998/index.html") {
                self?.webView.load(URLRequest(url: url))
            }
        }
    }

    func startKernelDaemon() {
        guard let url = URL(string: "http://127.0.0.1:8998/api/status") else { return }
        var request = URLRequest(url: url)
        request.timeoutInterval = 0.5

        let task = URLSession.shared.dataTask(with: request) { [weak self] (data, response, error) in
            if error != nil || (response as? HTTPURLResponse)?.statusCode != 200 {
                self?.launchPythonDaemon()
            }
        }
        task.resume()
    }

    func launchPythonDaemon() {
        let bundlePath = Bundle.main.bundlePath
        let possiblePaths = [
            (bundlePath as NSString).appendingPathComponent("Contents/Resources/src/main.py"),
            "/Users/silversurfer/Documents/Omniverse2/apps/omniverse_os/src/main.py"
        ]
        
        for scriptPath in possiblePaths {
            if FileManager.default.fileExists(atPath: scriptPath) {
                let p = Process()
                p.executableURL = URL(fileURLWithPath: "/usr/bin/python3")
                p.arguments = [scriptPath]
                p.standardOutput = nil
                p.standardError = nil
                try? p.run()
                self.process = p
                break
            }
        }
    }

    func windowWillClose(_ notification: Notification) {
        process?.terminate()
        NSApp.terminate(nil)
    }
}

class AppDelegate: NSObject, NSApplicationDelegate {
    var windowController: MainWindowController?

    func applicationDidFinishLaunching(_ notification: Notification) {
        NSApp.setActivationPolicy(.regular)
        windowController = MainWindowController()
        windowController?.showWindow(nil)
        NSApp.activate(ignoringOtherApps: true)
    }

    func applicationShouldTerminateAfterLastWindowClosed(_ sender: NSApplication) -> Bool {
        return true
    }
}

let app = NSApplication.shared
let delegate = AppDelegate()
app.delegate = delegate
app.run()
