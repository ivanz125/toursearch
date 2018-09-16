package tours.model;

import javax.persistence.*;
import java.util.Date;

@Entity
@Table(name = "monitoring")
public class Monitoring {
    @Id
    @GeneratedValue(strategy=GenerationType.AUTO)
    private Integer id;

    private Integer userId;

    private Boolean active;

    private Integer interval;

    private Date nextUpdate;

    private Date expires;

    private Date nextEmail;

    public Integer getId() {
        return id;
    }

    public void setId(Integer id) {
        this.id = id;
    }

    public Integer getUserId() {
        return userId;
    }

    public void setUserId(Integer userId) {
        this.userId = userId;
    }

    public Boolean getActive() {
        return active;
    }

    public void setActive(Boolean active) {
        this.active = active;
    }

    public Integer getInterval() {
        return interval;
    }

    public void setInterval(Integer interval) {
        this.interval = interval;
    }

    public Date getNextUpdate() {
        return nextUpdate;
    }

    public void setNextUpdate(Date nextUpdate) {
        this.nextUpdate = nextUpdate;
    }

    public Date getExpires() {
        return expires;
    }

    public void setExpires(Date expires) {
        this.expires = expires;
    }

    public Date getNextEmail() {
        return nextEmail;
    }

    public void setNextEmail(Date nextEmail) {
        this.nextEmail = nextEmail;
    }
}
