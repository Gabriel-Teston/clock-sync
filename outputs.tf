output "instance_a_ip_addr" {
  value = google_compute_address.static_a.address
}

output "instance_b_ip_addr" {
  value = google_compute_address.static_b.address
}

output "instance_c_ip_addr" {
  value = google_compute_address.static_c.address
}
