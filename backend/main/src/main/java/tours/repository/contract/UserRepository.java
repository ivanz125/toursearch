package tours.repository.contract;

import tours.model.User;
import org.springframework.stereotype.Repository;

@Repository
public interface UserRepository {
    User getUserByLogin(String email, String passwordMd5);
    User registerUser(String firstName, String lastName, String email, String passwordMd5);
}
