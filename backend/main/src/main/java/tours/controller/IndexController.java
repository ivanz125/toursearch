package tours.controller;

import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
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

    @GetMapping("/bus")
    public String pageBus() {
        return "bus";
    }

    @GetMapping("/monitoring_list")
    public String pageMonitoringList() {
        return "monitoring_list";
    }

    @GetMapping("/monitoring")
    public String pageMonitoring(Model model,
                                 @RequestParam(value = "id") int id) {
        model.addAttribute("monitoring_id", id);
        return "monitoring";
    }
}
