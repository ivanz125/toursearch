package tours.email;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.mail.SimpleMailMessage;
import org.springframework.mail.javamail.JavaMailSender;
import org.springframework.stereotype.Component;

@Component
public class EmailServiceImpl implements EmailService {

    private final JavaMailSender mailSender;

    @Autowired
    public EmailServiceImpl(JavaMailSender mailSender) {
        this.mailSender = mailSender;
    }

    @Override
    public void sendMessage(String email, String monitoringName, int resultsCount) {
        SimpleMailMessage message = new SimpleMailMessage();
        message.setTo("ivanzh125@gmail.com");
        message.setFrom("toursearch0@gmail.com");
        message.setSubject(String.format("Мониторинг \"%s\"", monitoringName));
        message.setText(String.format("Найдено %s результатов по заданным параметрам. Войдите в систему чтобы их просмотреть.", resultsCount));
        mailSender.send(message);
    }
}
