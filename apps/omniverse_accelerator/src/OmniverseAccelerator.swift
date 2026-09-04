//
//  OmniverseAccelerator.swift
//  Omniverse OS - Native macOS Standalone Application Pro
//  Author: Charlotte Duval & Viktor Vance
//  Pod: Pod 16 (macOS Systems Division)
//

import Cocoa
import WebKit

class MainWindowController: NSWindowController, NSWindowDelegate {
    var webView: WKWebView!
    var process: Process?

    convenience init() {
        let window = NSWindow(
            contentRect: NSRect(x: 0, y: 0, width: 1200, height: 780),
            styleMask: [.titled, .closable, .miniaturizable, .resizable, .fullSizeContentView],
            backing: .buffered,
            defer: false
        )
        self.init(window: window)
        
        window.title = "Omniverse OS: Hardware Accelerator Pro"
        window.titleVisibility = .hidden
        window.titlebarAppearsTransparent = true
        window.styleMask.insert(.fullSizeContentView)
        window.isMovableByWindowBackground = true
        window.appearance = NSAppearance(named: .darkAqua)
        window.backgroundColor = NSColor(calibratedRed: 6/255, green: 9/255, blue: 14/255, alpha: 1.0)
        window.center()
        window.delegate = self

        // WKWebView Configuration
        let config = WKWebViewConfiguration()
        config.preferences.setValue(true, forKey: "developerExtrasEnabled")
        
        webView = WKWebView(frame: window.contentView!.bounds, configuration: config)
        webView.autoresizingMask = [.width, .height]
        webView.setValue(false, forKey: "drawsBackground")
        window.contentView?.addSubview(webView)

        // Ensure background daemon is running
        startBackgroundDaemon()

        // Load Dashboard
        DispatchQueue.main.asyncAfter(deadline: .now() + 0.3) { [weak self] in
            if let url = URL(string: "http://localhost:8990/index.html") {
                self?.webView.load(URLRequest(url: url))
            }
        }
    }

    func startBackgroundDaemon() {
        guard let url = URL(string: "http://localhost:8990/api/status") else { return }
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
        let pythonScript = (bundlePath as NSString).appendingPathComponent("Contents/Resources/src/main.py")
        
        if FileManager.default.fileExists(atPath: pythonScript) {
            let p = Process()
            p.executableURL = URL(fileURLWithPath: "/usr/bin/python3")
            p.arguments = [pythonScript]
            p.standardOutput = nil
            p.standardError = nil
            try? p.run()
            self.process = p
        }
    }

    func windowWillClose(_ notification: Notification) {
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
