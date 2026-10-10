package com.agri.portal.repository;

import com.agri.portal.dto.QueryLog;
import org.springframework.data.jpa.repository.JpaRepository;

/** Simple repository for query logs (H2). */
public interface QueryLogRepository extends JpaRepository<QueryLog, Long> {
}
