def print_file(file_path):
  with open(file_path, "r") as f:
    text = f.read()
    print(f"""
      <div class="container">
        <div class="row">
          <div class="col-md-12">
            <h1>{file_path}</h1>
            <p>{text}</p>
          </div>
        </div>
      </div>
    """)