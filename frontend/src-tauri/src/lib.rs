use std::net::TcpStream;
use std::process::{Child, Command};
use std::sync::{Arc, Mutex};
use std::time::Duration;

fn is_server_alive() -> bool {
    TcpStream::connect_timeout(
        &"127.0.0.1:8000".parse().unwrap(),
        Duration::from_millis(300),
    )
    .is_ok()
}

fn try_spawn_server() -> Option<Child> {
    if is_server_alive() {
        println!("[Pramaan Tauri] API server is already active on 127.0.0.1:8000");
        return None;
    }

    println!("[Pramaan Tauri] API server not detected. Spawning local server...");

    let cwd = std::env::current_dir().unwrap_or_default();
    let exe_dir = std::env::current_exe()
        .ok()
        .and_then(|p| p.parent().map(|p| p.to_path_buf()))
        .unwrap_or_default();

    let candidate_roots = [
        cwd.clone(),
        cwd.join(".."),
        cwd.join("../.."),
        exe_dir.clone(),
        exe_dir.join(".."),
        exe_dir.join("../.."),
        std::path::PathBuf::from("/mnt/work/projects/Quantlab"),
    ];

    let mut project_root = None;
    let mut python_bin = None;

    for root in &candidate_roots {
        let venv_py = root.join("venv/bin/python");
        let venv3_py = root.join("venv/bin/python3");
        let src_api = root.join("src/api/main.py");

        if src_api.exists() {
            project_root = Some(root.clone());
            if venv_py.exists() {
                python_bin = Some(venv_py.to_string_lossy().to_string());
                break;
            } else if venv3_py.exists() {
                python_bin = Some(venv3_py.to_string_lossy().to_string());
                break;
            }
        }
    }

    let root = project_root.unwrap_or(cwd);
    let py = python_bin.unwrap_or_else(|| "python3".to_string());

    println!("[Pramaan Tauri] Launching backend using {:?} from working dir {:?}", py, root);

    match Command::new(&py)
        .args(["-m", "src.api.main"])
        .current_dir(&root)
        .spawn()
    {
        Ok(child) => {
            println!("[Pramaan Tauri] Spawned backend server (PID: {})", child.id());
            for _ in 0..30 {
                std::thread::sleep(Duration::from_millis(200));
                if is_server_alive() {
                    println!("[Pramaan Tauri] API server ready on http://127.0.0.1:8000");
                    break;
                }
            }
            Some(child)
        }
        Err(e) => {
            eprintln!("[Pramaan Tauri] Failed to spawn python backend: {}", e);
            None
        }
    }
}

#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    let server_child: Arc<Mutex<Option<Child>>> = Arc::new(Mutex::new(None));
    let server_child_clone = server_child.clone();

    let app = tauri::Builder::default()
        .setup(move |app| {
            if cfg!(debug_assertions) {
                app.handle().plugin(
                    tauri_plugin_log::Builder::default()
                        .level(log::LevelFilter::Info)
                        .build(),
                )?;
            }
            let child = try_spawn_server();
            if let Some(c) = child {
                let mut guard = server_child_clone.lock().unwrap();
                *guard = Some(c);
            }
            Ok(())
        })
        .build(tauri::generate_context!())
        .expect("error while building tauri application");

    app.run(move |_app_handle, event| {
        if let tauri::RunEvent::ExitRequested { .. } | tauri::RunEvent::Exit = event {
            let mut guard = server_child.lock().unwrap();
            if let Some(mut child) = guard.take() {
                println!("[Pramaan Tauri] Terminating background server PID {}...", child.id());
                let _ = child.kill();
            }
        }
    });
}
