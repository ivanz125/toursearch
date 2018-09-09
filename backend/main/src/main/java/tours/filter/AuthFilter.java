package tours.filter;

import org.springframework.stereotype.Component;
import org.springframework.web.filter.GenericFilterBean;

import javax.servlet.*;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import javax.servlet.http.HttpSession;
import java.io.IOException;

@Component
public class AuthFilter extends GenericFilterBean {

    @Override
    public void doFilter(ServletRequest servletRequest, ServletResponse servletResponse, FilterChain filterChain) throws IOException, ServletException {
        HttpServletRequest req = (HttpServletRequest) servletRequest;

        if ("POST".equals(req.getMethod())|| "/favicon.ico".equals(req.getServletPath()) || "/login".equals(req.getServletPath()) ||
                req.getServletPath().startsWith("/css") || req.getServletPath().startsWith("/js") ||
                req.getServletPath().startsWith("/static") || req.getServletPath().startsWith("/api")) {
            filterChain.doFilter(servletRequest, servletResponse);
            return;
        }

        HttpSession session = req.getSession();
        if (session == null || session.getAttribute("user") == null) {
            HttpServletResponse resp = (HttpServletResponse) servletResponse;
            System.out.println(req.getServletPath() + " : not authorized");
            resp.sendRedirect("/login");
        } else {
            filterChain.doFilter(servletRequest, servletResponse);
        }
    }
}
