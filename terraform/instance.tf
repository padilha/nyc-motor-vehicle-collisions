# Ref: https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/compute_instance
resource "google_compute_instance" "default" {
  name         = var.instance_name
  machine_type = "e2-standard-4"
  zone         = var.zone

  boot_disk {
    initialize_params {
      image = "ubuntu-os-cloud/ubuntu-2204-lts"
      size  = 30
    }
  }

  network_interface {
    network = "default"
    access_config {}
  }

  metadata_startup_script = <<-EOF
    sudo apt update
    sudo apt install python3-pip -y
    sudo apt install docker.io -y
    sudo usermod -aG docker $USER
    sudo chmod 666 /var/run/docker.sock # see https://stackoverflow.com/questions/48957195/how-to-fix-docker-got-permission-denied-issue
    pip3 install -r pandas==1.5.2 prefect-gcp[cloud_storage]==0.2.4 protobuf==4.21.11 pyarrow==10.0.1 pandas-gbq==0.18.1
    export PATH="$HOME/.local/bin:$PATH" # to be able to execute prefect
    prefect cloud login -k ${var.prefect_api_key}
    EOF
}