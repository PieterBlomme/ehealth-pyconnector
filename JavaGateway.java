import py4j.GatewayServer;
import java.util.*;
import java.io.*;
import org.w3c.dom.Element;
import oasis.names.tc.saml._2_0.protocol.AttributeQuery;
import be.ehealth.technicalconnector.config.ConfigFactory;
import be.ehealth.technicalconnector.service.sts.domain.SAMLAttribute;
import be.ehealth.technicalconnector.service.sts.domain.SAMLAttributeDesignator;
import be.ehealth.technicalconnector.service.sts.security.SAMLToken;
import be.ehealth.technicalconnector.session.Session;
import be.ehealth.technicalconnector.session.SessionManager;
import be.ehealth.technicalconnector.config.ConfigValidator;
import be.ehealth.businessconnector.genericasync.mappers.CommonInputMapper;
import org.mapstruct.factory.Mappers;
import be.ehealth.businessconnector.test.testcommons.utils.FileTestUtils;

public class JavaGateway {

  public static void main(String[] args) throws Exception {
    JavaGateway app = new JavaGateway();
    // app is now the gateway.entry_point
    GatewayServer server = new GatewayServer(app);
    System.out.println("Started");
    server.start();
  }

  public ConfigValidator getConfigValidator(){
    return ConfigFactory.getConfigValidator();
  }

  public ArrayList<SAMLAttributeDesignator> createAttributeDesignatorList(){
    // This causes issues if done outside Java program due to type conversion
    return new ArrayList<SAMLAttributeDesignator>();
  }

  public ArrayList<SAMLAttribute> createSAMLAttributeList(){
    // This causes issues if done outside Java program due to type conversion
    return new ArrayList<SAMLAttribute>();
  }

  public SAMLAttribute createSAMLAttribute(String v1, String v2, String v3) {
    // This causes issues if done outside Java program due to type conversion
    return new SAMLAttribute(v1, v2, v3);
  }

  public Map<String, Object> createHashMap(){
    return new HashMap<String, Object>();
  }

  public AttributeQuery createAttributeQueryFromTemplate(Map<String, Object> testFileParams, String requestLocation) throws Exception {
      return FileTestUtils.toObject(testFileParams, requestLocation, AttributeQuery.class);
  }

  public CommonInputMapper getCommontInputMapper(){
    return Mappers.getMapper(
                CommonInputMapper.class
            );
  }
}