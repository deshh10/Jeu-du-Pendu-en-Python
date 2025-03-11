package me.topeestla.hangmangame.repository;

import me.topeestla.hangmangame.entity.User;
import org.springframework.data.repository.CrudRepository;

import java.util.Optional;

/**
 * @author TopeEstLa
 */
public interface UserRepository extends CrudRepository<User, Integer> {

    Optional<User> findByUsername(String username);
}
