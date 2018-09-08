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
import org.springframework.web.bind.annotation.ResponseBody;

import javax.servlet.http.HttpSession;

@Controller
public class LoginController {

    private UserRepository userRepository;

    @Autowired
    public LoginController(UserRepository userRepository) {
        this.userRepository = userRepository;
    }

    @GetMapping("/login")
    public String page(Model model) {
        return "login";
    }

    @PostMapping("/login")
    public @ResponseBody String loginUser(@RequestParam(name="email") String email,
                                          @RequestParam(name="password") String password,
                                          HttpSession session) {
        password = Utils.md5(password);
        if (password == null) return "Exception";

        User user = userRepository.getUserByLogin(email, password);
        if (user != null) {
            session.setAttribute("user", user);
            session.setMaxInactiveInterval(10);
            return "OK";
        }
        return "Not OK";
    }
}
