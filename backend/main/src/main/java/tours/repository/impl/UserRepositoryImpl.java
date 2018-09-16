package tours.repository.impl;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.transaction.annotation.Transactional;
import tours.model.User;
import tours.repository.contract.UserRepository;
import org.springframework.stereotype.Repository;

import javax.persistence.EntityManager;
import javax.persistence.PersistenceContext;
import javax.persistence.Query;
import java.util.List;

@Repository
public class UserRepositoryImpl implements UserRepository {

    private static final Logger log = LoggerFactory.getLogger(UserRepositoryImpl.class);

    @PersistenceContext
    private EntityManager entityManager;

    @Override
    public User getUserByLogin(String email, String passwordMd5) {
        Query query = entityManager.createNativeQuery("SELECT * FROM users WHERE email=:e AND password=:p", User.class);
        query.setParameter("e", email);
        query.setParameter("p", passwordMd5);
        List users = query.getResultList();
        if (users == null || users.size() == 0) return null;
        return (User) users.get(0);
    }

    @Override
    public User getUserById(int id) {
        Query query = entityManager.createNativeQuery("SELECT * FROM users WHERE id=:uid", User.class);
        query.setParameter("uid", id);
        List users = query.getResultList();
        if (users == null || users.size() == 0) return null;
        return (User) users.get(0);
    }

    @Transactional
    @Override
    public User registerUser(String firstName, String lastName, String email, String passwordMd5) {
        String q = "SELECT * from `users` WHERE email = :email ORDER BY id DESC LIMIT 1";
        Query userQuery = entityManager.createNativeQuery(q, User.class);
        userQuery.setParameter("email", email);
        List r = userQuery.getResultList();
        if (r != null && r.size() > 0) {
            log.info("User with email " + email + " already exists");
            User user = new User();
            user.setId(-1);
            return user;
        }

        q = "INSERT INTO `users` (`first_name`, `last_name`, `email`, `password`) VALUES (:fn, :ln, :email, :pwd)";
        Query query = entityManager.createNativeQuery(q, User.class);
        query.setParameter("fn", firstName);
        query.setParameter("ln", lastName);
        query.setParameter("email", email);
        query.setParameter("pwd", passwordMd5);
        query.executeUpdate();
        // Get inserted id
        q = "SELECT * from `users` WHERE email=:email ORDER BY id DESC LIMIT 1";
        Query idQuery = entityManager.createNativeQuery(q, User.class);
        idQuery.setParameter("email", email);
        r = idQuery.getResultList();
        if (r != null && r.size() > 0) {
            log.info("Successfully registered " + firstName + " " + lastName + " with email " + email);
            return ((User) r.get(0));
        }
        log.error("Failed to register " + firstName + " " + lastName + " with email " + email);
        return null;
    }
}
