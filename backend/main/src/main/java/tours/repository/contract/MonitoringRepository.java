package tours.repository.contract;

import org.springframework.stereotype.Repository;
import tours.model.Monitoring;
import tours.model.User;

import java.util.List;

@Repository
public interface MonitoringRepository {
    List<Monitoring> getAllActiveMonitorings();
    List<Monitoring> getMonitoringsByUser(int userId);
    int createMonitoring(Monitoring monitoring);
    void updateMonitoringUpdateTime(Monitoring monitoring);
    void setMonitoringActive(int monitoringId, boolean setActive);
}
