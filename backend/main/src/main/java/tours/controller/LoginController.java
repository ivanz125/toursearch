package tours.controller;

import tours.model.User;
import tours.repository.contract.UserRepository;
import tours.util.Utils;
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
            session.setMaxInactiveInterval(3600);
            return "redirect:avia";
        }
        model.addAttribute("bad_password", true);
        return "login";
    }

    @GetMapping("/register")
    public String register() {
        return "registration";
    }

    @PostMapping("/register")
    public String registerUser(@RequestParam(name="first_name") String firstName,
                               @RequestParam(name="last_name") String lastName,
                               @RequestParam(name="email") String email,
                               @RequestParam(name="password") String password,
                               HttpSession session,
                               Model model) {
        User user = userRepository.registerUser(firstName, lastName, email, password);
        if (user != null && user.getId() == -1) {
            model.addAttribute("error", 1);
            return "registration";
        }
        if (user == null) {
            model.addAttribute("error", 2);
            return "registration";
        }
        session.setAttribute("user", user);
        session.setAttribute("user_name", String.format("%s %s", user.getFirstName(), user.getLastName()));
        session.setMaxInactiveInterval(3600);
        return "redirect:avia";
    }
}
