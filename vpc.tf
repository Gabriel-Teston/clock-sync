resource "google_compute_network" "vpc_network" {
  name = "terraform-network"
}

resource "google_compute_firewall" "web" {
  name    = "web-firewall"
  network = google_compute_network.vpc_network.name

  allow {
    protocol = "tcp"
    ports    = ["80", "8080", "1000-5000", "50051"]
  }
}

resource "google_compute_firewall" "ssh" {
  name    = "ssh-firewall"
  network = google_compute_network.vpc_network.name

  allow {
    protocol = "tcp"
    ports    = ["22"]
  }
}

resource "google_compute_address" "static_a" {
  name = "ipv4-address-a"
}

resource "google_compute_address" "static_b" {
  name = "ipv4-address-b"
}

resource "google_compute_address" "static_c" {
  name = "ipv4-address-c"
}