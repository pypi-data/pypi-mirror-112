include:
  - ..letsencrypt

letsencrypt-activate-cert:
  file.symlink:
    - name: /etc/odoopbx/pki/current
    - target: /etc/letsencrypt/live/odoopbx
    - onlyif:
        fun: x509.read_certificate
        certificate: /etc/letsencrypt/live/odoopbx/cert.pem
