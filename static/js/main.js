/* Ridgane Excavation — main.js (vanilla) */
(function () {
  "use strict";

  // ---- Footer year ----
  var yearEl = document.getElementById("year");
  if (yearEl) yearEl.textContent = new Date().getFullYear();

  // ---- Mobile nav toggle ----
  var navToggle = document.getElementById("navToggle");
  var navLinks = document.getElementById("navLinks");
  if (navToggle && navLinks) {
    navToggle.addEventListener("click", function () {
      var open = navLinks.classList.toggle("open");
      navToggle.setAttribute("aria-expanded", open ? "true" : "false");
      navToggle.setAttribute("aria-label", open ? "Close menu" : "Open menu");
    });
    // Close when a nav link is clicked (mobile)
    navLinks.querySelectorAll("a").forEach(function (link) {
      link.addEventListener("click", function () {
        navLinks.classList.remove("open");
        navToggle.setAttribute("aria-expanded", "false");
      });
    });
  }

  // ---- Smooth scroll for anchor links (native fallback aside) ----
  document.querySelectorAll('a[href^="#"]').forEach(function (anchor) {
    anchor.addEventListener("click", function (e) {
      var targetId = this.getAttribute("href");
      if (targetId.length < 2) return;
      var target = document.querySelector(targetId);
      if (!target) return;
      e.preventDefault();
      var y = target.getBoundingClientRect().top + window.pageYOffset - 70;
      window.scrollTo({ top: y, behavior: "smooth" });
    });
  });

  // ---- Project filter ----
  var filters = document.querySelectorAll(".filters .filter");
  var projects = document.querySelectorAll(".project");
  if (filters.length && projects.length) {
    filters.forEach(function (btn) {
      btn.addEventListener("click", function () {
        var filterVal = btn.getAttribute("data-filter");
        filters.forEach(function (f) { f.classList.remove("active"); f.setAttribute("aria-selected", "false"); });
        btn.classList.add("active");
        btn.setAttribute("aria-selected", "true");
        projects.forEach(function (p) {
          var cat = p.getAttribute("data-cat") || "";
          var show = filterVal === "all" || cat === filterVal;
          p.classList.toggle("hide", !show);
        });
      });
    });
  }

  // ---- Quote form: validate + send to the Mailgun relay ----
  var form = document.getElementById("quoteForm");
  var note = document.getElementById("formNote");
  if (form) {
    function markInvalid(field, bad) {
      field.classList.toggle("invalid", !!bad);
      return bad;
    }

    var submitBtn = form.querySelector("button[type=submit]");

    form.addEventListener("submit", function (e) {
      e.preventDefault();

      // Honeypot: bots fill the hidden field -> fake success, send nothing.
      var hp = form.querySelector('[name="company_website"]');
      if (hp && hp.value !== "") {
        note.className = "form-note ok";
        note.textContent = "Thanks! Your request has been received. We'll call you within one business day.";
        form.reset();
        return;
      }

      var name = document.getElementById("qName");
      var phone = document.getElementById("qPhone");
      var email = document.getElementById("qEmail");
      var service = document.getElementById("qService");
      var message = document.getElementById("qMessage");

      var ok = true;
      var nameValid = name.value.trim().length >= 2;
      ok = markInvalid(name, !nameValid) === false && ok;

      var phoneValid = phone.value.replace(/[^\d]/g, "").length >= 10;
      ok = markInvalid(phone, !phoneValid) === false && ok;

      var emailValid = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.value);
      ok = markInvalid(email, !emailValid) === false && ok;

      var serviceValid = service.value !== "";
      ok = markInvalid(service, !serviceValid) === false && ok;

      var fields = [name, phone, email, service, message];
      fields.forEach(function (f) {
        f.addEventListener("input", function () { note.classList.remove("ok", "err"); note.textContent = ""; });
      });

      if (!ok) {
        note.className = "form-note err";
        note.textContent = "Please fill in the required fields correctly.";
        return;
      }

      // Send via the site's own API relay (server holds the Mailgun key).
      submitBtn.disabled = true;
      submitBtn.textContent = "Sending\u2026";
      note.textContent = "";

      fetch("/api/contact", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          name: name.value.trim(),
          email: email.value.trim(),
          phone: phone.value.trim(),
          service: service.value,
          message: (message.value || "").trim()
        })
      })
        .then(function (r) {
          return r.json().catch(function () { return {}; }).then(function (j) { return { ok: r.ok, body: j }; });
        })
        .then(function (res) {
          if (!res.ok) throw new Error(res.body.error || "HTTP error");
          note.className = "form-note ok";
          note.textContent = "Thanks " + name.value.trim().split(" ")[0] + "! Your request has been sent. We'll call you within one business day.";
          form.reset();
        })
        .catch(function () {
          note.className = "form-note err";
          note.textContent = "Hmm, that didn't go through. Call or text 740-629-7020 and we'll pick it up there.";
        })
        .finally(function () {
          submitBtn.disabled = false;
          submitBtn.textContent = "Send My Request";
        });
    });
  }
})();