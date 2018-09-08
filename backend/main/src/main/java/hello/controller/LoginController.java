package hello.controller;

import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;

@Controller
public class LoginController {

    @GetMapping("/login")
    public String page(Model model) {
        return "login";
    }

    @PostMapping("/login")
    public String loginUser(@RequestParam(name="email") String email, @RequestParam(name="password") String password) {
        return "";
    }
}
