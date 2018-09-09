package tours.controller;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;

import javax.servlet.http.HttpSession;

@Controller
public class LogoutController {

    @GetMapping("/logout")
    public String loginUser(HttpSession session) {
        session.removeAttribute("user");
        session.removeAttribute("user_name");
        return "redirect:login";
    }
}
