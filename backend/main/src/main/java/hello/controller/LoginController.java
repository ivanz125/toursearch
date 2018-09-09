package hello.controller;

import hello.model.User;
import hello.repository.contract.UserRepository;
import hello.util.Utils;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;

import javax.servlet.http.HttpSession;

@Controller
public class LoginController {

    private UserRepository userRepository;

    @Autowired
    public LoginController(UserRepository userRepository) {
        this.userRepository = userRepository;
    }

    @GetMapping("/login")
    public String page() {
        return "login";
    }

    @PostMapping("/login")
    public String loginUser(@RequestParam(name="email") String email,
                            @RequestParam(name="password") String password,
                            HttpSession session,
                            Model model) {
        password = Utils.md5(password);
        if (password == null) return "login";

        User user = userRepository.getUserByLogin(email, password);
        if (user != null) {
            session.setAttribute("user", user);
            session.setAttribute("user_name", String.format("%s %s", user.getFirstName(), user.getLastName()));
            session.setMaxInactiveInterval(60);
            return "redirect:avia";
        }
        model.addAttribute("bad_password", true);
        return "login";
    }
}
