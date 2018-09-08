package hello.repository.impl;

import hello.model.User;
import hello.repository.contract.UserRepository;
import org.springframework.stereotype.Repository;

import javax.persistence.EntityManager;
import javax.persistence.PersistenceContext;
import javax.persistence.Query;
import java.util.List;

@Repository
public class UserRepositoryImpl implements UserRepository {

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
}
