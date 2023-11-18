package com.crio.starter.repository;

 
import java.util.Optional;
import com.crio.starter.data.GreetingsEntity;
import org.springframework.data.mongodb.repository.MongoRepository;

public interface GreetingsRepository extends MongoRepository<GreetingsEntity, String> {
 
  Optional<GreetingsEntity> findById(String id);

  Optional<GreetingsEntity> findByNameAndUrlAndCaption(String name, String url, String caption);


  // List<GreetingsEntity> findAll();
}