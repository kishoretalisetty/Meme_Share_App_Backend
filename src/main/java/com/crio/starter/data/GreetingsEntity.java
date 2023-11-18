package com.crio.starter.data;

import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.NonNull;
import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.Document;

@Data
@Document(collection = "greetings")
@NoArgsConstructor
public class GreetingsEntity {

  @Id
  private String id;
  @NonNull
  private String name;
  @NonNull
  private String url;
  @NonNull
  private String caption;
  public String getId() {
    return this.id;
  }


}