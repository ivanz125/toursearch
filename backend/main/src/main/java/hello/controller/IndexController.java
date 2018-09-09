package hello.controller;

import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;

import javax.servlet.http.HttpSession;

@Controller
public class IndexController {

    @GetMapping("/")
    public String page(HttpSession session) {
        if (session.getAttribute("user") != null) return "redirect:avia";
        return "redirect:login";
    }

    @GetMapping("/avia")
    public String pageAvia() {
        return "avia";
    }
}
