package tours.scheduling;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.node.ObjectNode;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpMethod;
import org.springframework.http.MediaType;
import org.springframework.http.converter.StringHttpMessageConverter;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Component;
import org.springframework.web.client.RestTemplate;
import org.springframework.web.util.UriComponentsBuilder;
import tours.email.EmailService;
import tours.model.Monitoring;
import tours.model.User;
import tours.repository.contract.MonitoringRepository;
import tours.repository.contract.UserRepository;

import java.nio.charset.Charset;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.List;

@Component
public class MonitoringScheduler {

    private static final Logger log = LoggerFactory.getLogger(MonitoringScheduler.class);

    private static final SimpleDateFormat dateFormat = new SimpleDateFormat("HH:mm:ss");

    private MonitoringRepository monitoringRepository;
    private UserRepository userRepository;
    private EmailService emailService;

    @Autowired
    public MonitoringScheduler(MonitoringRepository monitoringRepository, UserRepository userRepository, EmailService emailService) {
        this.monitoringRepository = monitoringRepository;
        this.userRepository = userRepository;
        this.emailService = emailService;
    }

    @Scheduled(fixedRate = 60000)
    public void monitorings() {
        List<Monitoring> monitoringList = monitoringRepository.getAllActiveMonitorings();
        if (monitoringList == null) {
            log.info("Monitoring list is null");
            return;
        }

        Date now = new Date();
        for (Monitoring monitoring : monitoringList) {
            // null could be if executing monitoring for the first time
            // .before indicates that update time already passed and execution required
            if (monitoring.getActive() && (monitoring.getNextUpdate() == null || monitoring.getNextUpdate().before(now))) {
                log.info("Executing monitoring: id=" + monitoring.getId());
                // Execute (send request to search server)
                RestTemplate restTemplate = new RestTemplate();
                restTemplate.getMessageConverters()
                        .add(0, new StringHttpMessageConverter(Charset.forName("UTF-8")));
                UriComponentsBuilder builder = UriComponentsBuilder.fromHttpUrl("http://127.0.0.1:5000/monitoring/execute")
                        .queryParam("id", monitoring.getId());
                HttpHeaders headers = new HttpHeaders();
                headers.set("Accept", MediaType.APPLICATION_JSON_VALUE);
                HttpEntity<?> entity = new HttpEntity<>(headers);
                HttpEntity<String> response = restTemplate.exchange(
                        builder.toUriString(),
                        HttpMethod.GET,
                        entity,
                        String.class);

                // Parse and log response
                ObjectMapper mapper = new ObjectMapper();
                try {
                    ObjectNode node = mapper.readValue(response.getBody(), ObjectNode.class);
                    if (node != null) {
                        int resultsCount = node.has("results") ? node.get("results").asInt() : -1;
                        String msg = String.format("Monitoring id=%d executed. Results count: %d.", monitoring.getId(), resultsCount);
                        if (node.has("error")) msg += String.format(" Error: %s", node.get("error").asText());
                        log.info(msg);

                        // Send email if required
                        if (monitoring.getNextEmail() == null || monitoring.getNextEmail().before(now) && resultsCount > 0) {
                            User user = userRepository.getUserById(monitoring.getUserId());
                            String name = node.has("name") ? node.get("name").asText() : "Unknown";
                            emailService.sendMessage(user.getEmail(), name, resultsCount);
                        }
                    }
                }
                catch (Exception ex) {
                    log.error(ex.getMessage());
                }

                // Reschedule monitoring
                monitoringRepository.updateMonitoringUpdateTime(monitoring);
            }
        }
    }

    @Scheduled(fixedRate = 600000)
    public void emails() {

    }
}
