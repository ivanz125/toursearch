package tours.repository.contract;

import tours.model.User;
import org.springframework.stereotype.Repository;

@Repository
public interface UserRepository {
    User getUserByLogin(String email, String passwordMd5);
    User getUserById(int id);
    User registerUser(String firstName, String lastName, String email, String passwordMd5);
}
