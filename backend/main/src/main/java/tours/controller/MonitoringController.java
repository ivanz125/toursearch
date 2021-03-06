package tours.controller;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.node.ArrayNode;
import com.fasterxml.jackson.databind.node.ObjectNode;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpMethod;
import org.springframework.http.MediaType;
import org.springframework.http.converter.StringHttpMessageConverter;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.client.RestTemplate;
import org.springframework.web.util.UriComponentsBuilder;
import tours.model.Monitoring;
import tours.repository.contract.MonitoringRepository;

import java.nio.charset.Charset;
import java.util.Date;

@RestController("/api/monitoring")
public class MonitoringController {

    private MonitoringRepository monitoringRepository;

    @Autowired
    public MonitoringController(MonitoringRepository monitoringRepository) {
        this.monitoringRepository = monitoringRepository;
    }

    @CrossOrigin(origins = "*")
    @RequestMapping(method = RequestMethod.GET, value = "api/monitoring/create/avia", produces = "application/json")
    public String createAviaMonitoring(@RequestParam(value = "code_country") String codeCountry,
                                       @RequestParam(value = "start_date_from") String startDateFrom,
                                       @RequestParam(value = "start_date_to") String startDateTo,
                                       @RequestParam(value = "adults") int adults,
                                       @RequestParam(value = "children") int children,
                                       @RequestParam(value = "b_day_1", required = false) String bDay1,
                                       @RequestParam(value = "b_day_2", required = false) String bDay2,
                                       @RequestParam(value = "nights_min") int nightsMin,
                                       @RequestParam(value = "nights_max") int nightsMax,
                                       @RequestParam(value = "meals") String meals,
                                       @RequestParam(value = "price_max") int priceMax,
                                       @RequestParam(value = "user_id") int userId,
                                       @RequestParam(value = "interval") int interval,
                                       @RequestParam(value = "price_limit") int priceLimit,
                                       @RequestParam(value = "name") String name) {
        // Create monitoring entry in MySQL DB
        Monitoring monitoring = new Monitoring();
        monitoring.setUserId(userId);
        monitoring.setActive(true);
        monitoring.setInterval(interval);
        Date exp = new Date();
        exp.setTime(System.currentTimeMillis() + 604800000); // One week ahead
        monitoring.setExpires(exp);
        int id = monitoringRepository.createMonitoring(monitoring);

        // Create monitoring object in MongoDB
        RestTemplate restTemplate = new RestTemplate();
        restTemplate.getMessageConverters()
                .add(0, new StringHttpMessageConverter(Charset.forName("UTF-8")));
        UriComponentsBuilder builder = UriComponentsBuilder.fromHttpUrl("http://127.0.0.1:5000/monitoring/create")
                .queryParam("code_country", codeCountry)
                .queryParam("start_date_from", startDateFrom)
                .queryParam("start_date_to", startDateTo)
                .queryParam("adults", adults)
                .queryParam("children", children)
                .queryParam("nights_min", nightsMin)
                .queryParam("nights_max", nightsMax)
                .queryParam("meals", meals)
                .queryParam("price_max", priceMax)
                .queryParam("price_limit", priceLimit)
                .queryParam("type", "avia")
                .queryParam("id", id)
                .queryParam("user_id", userId)
                .queryParam("name", name);
        if (children > 0 && bDay1 != null) builder.queryParam("b_day_1", bDay1);
        if (children > 1 && bDay2 != null) builder.queryParam("b_day_2", bDay2);

        HttpHeaders headers = new HttpHeaders();
        headers.set("Accept", MediaType.APPLICATION_JSON_VALUE);
        HttpEntity<?> entity = new HttpEntity<>(headers);
        HttpEntity<String> response = restTemplate.exchange(
                builder.toUriString(),
                HttpMethod.GET,
                entity,
                String.class);
        return response.getBody();
    }

    @CrossOrigin(origins = "*")
    @RequestMapping(method = RequestMethod.GET, value = "api/monitoring/get", produces = "application/json")
    public String getMonitoringsByUser(@RequestParam(value = "user_id") int userId) {
        RestTemplate restTemplate = new RestTemplate();
        restTemplate.getMessageConverters()
                .add(0, new StringHttpMessageConverter(Charset.forName("UTF-8")));
        UriComponentsBuilder builder = UriComponentsBuilder.fromHttpUrl("http://127.0.0.1:5000/monitoring/get")
                .queryParam("user_id", userId);

        HttpHeaders headers = new HttpHeaders();
        headers.set("Accept", MediaType.APPLICATION_JSON_VALUE);
        HttpEntity<?> entity = new HttpEntity<>(headers);
        HttpEntity<String> response = restTemplate.exchange(
                builder.toUriString(),
                HttpMethod.GET,
                entity,
                String.class);

        // Parse array
        try {
            ObjectMapper mapper = new ObjectMapper();
            JsonNode root = mapper.readTree(response.getBody());
            ArrayNode array = (ArrayNode) root.get("data");
            for (JsonNode o : array) addActiveField(o);
            return root.toString();
        }
        catch (Exception ex) {
            ex.printStackTrace();
            return response.getBody();
        }
    }

    @CrossOrigin(origins = "*")
    @RequestMapping(method = RequestMethod.GET, value = "api/monitoring/get_one", produces = "application/json")
    public String getOneMonitoring(@RequestParam(value = "id") int id) {
        RestTemplate restTemplate = new RestTemplate();
        restTemplate.getMessageConverters()
                .add(0, new StringHttpMessageConverter(Charset.forName("UTF-8")));
        UriComponentsBuilder builder = UriComponentsBuilder.fromHttpUrl("http://127.0.0.1:5000/monitoring/get_one")
                .queryParam("id", id);

        HttpHeaders headers = new HttpHeaders();
        headers.set("Accept", MediaType.APPLICATION_JSON_VALUE);
        HttpEntity<?> entity = new HttpEntity<>(headers);
        HttpEntity<String> response = restTemplate.exchange(
                builder.toUriString(),
                HttpMethod.GET,
                entity,
                String.class);
        return addActiveField(response.getBody());
    }

    @CrossOrigin(origins = "*")
    @RequestMapping(method = RequestMethod.GET, value = "api/monitoring/get_data", produces = "application/json")
    public String getOneMonitoringData(@RequestParam(value = "id") int id) {
        RestTemplate restTemplate = new RestTemplate();
        restTemplate.getMessageConverters()
                .add(0, new StringHttpMessageConverter(Charset.forName("UTF-8")));
        UriComponentsBuilder builder = UriComponentsBuilder.fromHttpUrl("http://127.0.0.1:5000/monitoring/get_data")
                .queryParam("id", id);

        HttpHeaders headers = new HttpHeaders();
        headers.set("Accept", MediaType.APPLICATION_JSON_VALUE);
        HttpEntity<?> entity = new HttpEntity<>(headers);
        HttpEntity<String> response = restTemplate.exchange(
                builder.toUriString(),
                HttpMethod.GET,
                entity,
                String.class);
        return response.getBody();
    }

    @CrossOrigin(origins = "*")
    @RequestMapping(method = RequestMethod.GET, value = "api/monitoring/set_active", produces = "application/json")
    public String setMonitoringActiveState(@RequestParam(value = "id") int id,
                                           @RequestParam(value = "active") boolean active) {
        monitoringRepository.setMonitoringActive(id, active);
        return "{\"result\":1}";
    }

    @CrossOrigin(origins = "*")
    @RequestMapping(method = RequestMethod.DELETE, value = "api/monitoring/delete", produces = "application/json")
    public String deleteMonitoring(@RequestParam(value = "id") int id) {
        monitoringRepository.deleteMonitoring(id);
        RestTemplate restTemplate = new RestTemplate();
        restTemplate.getMessageConverters()
                .add(0, new StringHttpMessageConverter(Charset.forName("UTF-8")));
        UriComponentsBuilder builder = UriComponentsBuilder.fromHttpUrl("http://127.0.0.1:5000/monitoring/delete")
                .queryParam("id", id);

        HttpHeaders headers = new HttpHeaders();
        headers.set("Accept", MediaType.APPLICATION_JSON_VALUE);
        HttpEntity<?> entity = new HttpEntity<>(headers);
        HttpEntity<String> response = restTemplate.exchange(
                builder.toUriString(),
                HttpMethod.GET,
                entity,
                String.class);

        return response.getBody();
    }

    private String addActiveField(String monitoringStr) {
        ObjectMapper mapper = new ObjectMapper();
        try {
            JsonNode jsonNode = mapper.readTree(monitoringStr);
            boolean isActive = monitoringRepository.getMonitoring(jsonNode.get("id").asInt()).getActive();
            ((ObjectNode) jsonNode).put("active", isActive);
            return jsonNode.toString();
        }
        catch (Exception ex) {
            ex.printStackTrace();
            return null;
        }
    }

    private void addActiveField(JsonNode monitoring) {
        try {
            boolean isActive = monitoringRepository.getMonitoring(monitoring.get("id").asInt()).getActive();
            ((ObjectNode) monitoring).put("active", isActive);
        }
        catch (Exception ex) {
            ex.printStackTrace();
        }
    }
}
