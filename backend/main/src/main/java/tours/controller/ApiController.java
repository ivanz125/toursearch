package tours.controller;

import org.springframework.http.*;
import org.springframework.http.converter.StringHttpMessageConverter;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.client.RestTemplate;
import org.springframework.web.util.UriComponentsBuilder;

import java.nio.charset.Charset;

@RestController("/api")
public class ApiController {

    // TODO: 10/09/2018 Remove Access-Control-Allow-Origin

    @CrossOrigin(origins = "*")
    @RequestMapping(method = RequestMethod.GET, value = "api/tours/avia", produces = "application/json")
    public String aviaTours(@RequestParam(value = "code_country") String codeCountry,
                           @RequestParam(value = "start_date_from") String startDateFrom,
                           @RequestParam(value = "start_date_to") String startDateTo,
                           @RequestParam(value = "adults") int adults,
                           @RequestParam(value = "children") int children,
                           @RequestParam(value = "b_day_1", required = false) String bDay1,
                           @RequestParam(value = "b_day_2", required = false) String bDay2,
                           @RequestParam(value = "nights_min") int nightsMin,
                           @RequestParam(value = "nights_max") int nightsMax,
                           @RequestParam(value = "meals") String meals,
                           @RequestParam(value = "price_max") int priceMax) {
        RestTemplate restTemplate = new RestTemplate();
        restTemplate.getMessageConverters()
                .add(0, new StringHttpMessageConverter(Charset.forName("UTF-8")));
        UriComponentsBuilder builder = UriComponentsBuilder.fromHttpUrl("http://127.0.0.1:5000/")
                .queryParam("code_country", codeCountry)
                .queryParam("start_date_from", startDateFrom)
                .queryParam("start_date_to", startDateTo)
                .queryParam("adults", adults)
                .queryParam("children", children)
                .queryParam("nights_min", nightsMin)
                .queryParam("nights_max", nightsMax)
                .queryParam("meals", meals)
                .queryParam("price_max", priceMax);
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
    @RequestMapping(method = RequestMethod.GET, value = "api/tours/bus", produces = "application/json")
    public String busTours(@RequestParam(value = "start_date_from") String startDateFrom,
                           @RequestParam(value = "start_date_to") String startDateTo,
                           @RequestParam(value = "days_min") int daysMin,
                           @RequestParam(value = "days_max") int daysMax,
                           @RequestParam(value = "price_max") int priceMax,
                           @RequestParam(value = "places_str", required = false) String places,
                           @RequestParam(value = "places_mode", required = false) String placesMode) {
        RestTemplate restTemplate = new RestTemplate();
        restTemplate.getMessageConverters()
                .add(0, new StringHttpMessageConverter(Charset.forName("UTF-8")));
        UriComponentsBuilder builder = UriComponentsBuilder.fromHttpUrl("http://127.0.0.1:5000/bus")
                .queryParam("start_date_from", startDateFrom)
                .queryParam("start_date_to", startDateTo)
                .queryParam("days_min", daysMin)
                .queryParam("days_max", daysMax)
                .queryParam("price_max", priceMax);
        if (places != null) {
            System.out.println(places);
            builder.queryParam("places_str", places);
            if (placesMode != null) builder.queryParam("places_mode", placesMode);
        }

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
    @RequestMapping(method = RequestMethod.GET, value = "api/tours/bus/get_one", produces = "application/json")
    public String oneBusTour(@RequestParam(value = "url") String url) {
        RestTemplate restTemplate = new RestTemplate();
        restTemplate.getMessageConverters()
                .add(0, new StringHttpMessageConverter(Charset.forName("UTF-8")));
        UriComponentsBuilder builder = UriComponentsBuilder.fromHttpUrl("http://127.0.0.1:5000/bus/get_one")
                .queryParam("url", url);

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
}
