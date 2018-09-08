package hello.repository.contract;

import hello.model.User;
import org.springframework.stereotype.Repository;

@Repository
public interface UserRepository {
    User getUserByLogin(String email, String passwordMd5);
}
