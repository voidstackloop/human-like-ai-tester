"""Lightweight mock test server demonstrating common human UX traps and vulnerabilities."""

import http.server
import urllib.parse
import time
import json


class MockAppHandler(http.server.BaseHTTPRequestHandler):
    """HTTP handler with realistic user experience flaws."""

    # Simulated database to test duplicate entries
    users_db = []
    orders_db = []

    def _send_html(self, content: str, status: int = 200):
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(content.encode("utf-8"))

    def _send_json(self, data: dict, status: int = 200):
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode("utf-8"))

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)

        if parsed.path == "/" or parsed.path == "/checkout":
            # Realistic form with intentionally flawed UX
            html = """<!DOCTYPE html>
<html>
<head>
    <title>QuickShop Checkout</title>
    <style>
        body { font-family: sans-serif; max-width: 600px; margin: 40px auto; padding: 20px; }
        .form-group { margin-bottom: 15px; }
        label { display: block; margin-bottom: 5px; font-weight: bold; }
        input[type="text"], input[type="email"] { width: 100%; padding: 8px; box-sizing: border-box; }
        .btn { padding: 10px 20px; cursor: pointer; border: none; font-size: 16px; margin-right: 10px; }
        .btn-submit { background: #0070f3; color: white; }
        .btn-cancel { background: #e0e0e0; color: #333; }
        .error-banner { background: #fee2e2; color: #b91c1c; padding: 12px; margin-bottom: 20px; display: none; }
    </style>
</head>
<body>
    <h1>Complete Your Order</h1>
    <p>Please enter your payment & delivery info.</p>

    <!-- INTENTIONAL FLAW 1: Cancel button right next to Submit with similar size -->
    <form action="/api/submit-order" method="POST">
        <div class="form-group">
            <label for="name">Full Name</label>
            <input type="text" id="name" name="name" required placeholder="e.g. Jane Doe">
        </div>

        <div class="form-group">
            <label for="email">Email Address</label>
            <input type="email" id="email" name="email" required placeholder="name@example.com">
        </div>

        <div class="form-group">
            <!-- INTENTIONAL FLAW 2: Strict backend expects raw digits only, no help text -->
            <label for="phone">Phone Number (Required)</label>
            <input type="text" id="phone" name="phone" required placeholder="5551234567">
        </div>

        <div class="form-group">
            <label for="amount">Order Amount ($)</label>
            <input type="text" id="amount" name="amount" value="49.99">
        </div>

        <div style="margin-top: 30px;">
            <button type="submit" class="btn btn-submit">Place Order</button>
            <button type="reset" class="btn btn-cancel">Cancel</button>
        </div>
    </form>
</body>
</html>"""
            self._send_html(html)

        elif parsed.path == "/api/status":
            self._send_json({"status": "healthy", "orders_count": len(self.orders_db)})

        else:
            self._send_html("<h1>404 Not Found</h1>", 404)

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)

        if parsed.path == "/api/submit-order":
            content_len = int(self.headers.get("Content-Length", 0))
            post_body = self.rfile.read(content_len).decode("utf-8")
            params = urllib.parse.parse_qs(post_body)

            phone = params.get("phone", [""])[0]
            name = params.get("name", [""])[0]
            amount = params.get("amount", [""])[0]

            # INTENTIONAL FLAW 2 TEST: Rejects if phone contains formatting like (555) or dashes!
            if "-" in phone or "(" in phone or "." in phone or " " in phone:
                # Fails strictly on common human formatting!
                self._send_json({
                    "error": "Invalid format",
                    "message": "Phone number must contain exactly 10 digits without formatting characters.",
                }, 400)
                return

            # INTENTIONAL FLAW 3: Artificial 1.5 second delay without locking submit button -> vulnerable to double submission
            time.sleep(1.2)

            order_id = len(self.orders_db) + 1
            order_record = {"order_id": order_id, "name": name, "phone": phone, "amount": amount, "timestamp": time.time()}
            self.orders_db.append(order_record)

            self._send_json({
                "success": True,
                "order_id": order_id,
                "message": "Order placed successfully!",
                "total_orders_in_db": len(self.orders_db),
            }, 200)

        elif parsed.path == "/api/users":
            content_len = int(self.headers.get("Content-Length", 0))
            body_raw = self.rfile.read(content_len).decode("utf-8")
            try:
                data = json.loads(body_raw)
                # INTENTIONAL FLAW 4: Fails if age is passed as string "25" rather than integer 25
                if "age" in data and not isinstance(data["age"], int):
                    self._send_json({"error": "Type error: age must be an integer, not string"}, 500)
                    return
                self.users_db.append(data)
                self._send_json({"id": len(self.users_db), "status": "created"}, 201)
            except Exception as e:
                self._send_json({"error": str(e)}, 400)
        else:
            self._send_json({"error": "Endpoint not found"}, 404)


def run_mock_server(port: int = 8088):
    """Run server synchronously."""
    server = http.server.HTTPServer(("0.0.0.0", port), MockAppHandler)
    print(f"[*] Human-Tester Mock Server running at http://localhost:{port}/")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n[*] Stopping server...")
        server.server_close()
